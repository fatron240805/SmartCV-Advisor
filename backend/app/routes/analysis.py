"""Routes for CV analysis history, result detail, and suggestions."""

# Định nghĩa route cho phân tích, so sánh kỹ năng và kết quả.

from fastapi import APIRouter, Depends, HTTPException, Query
from app.db import db  # Import instance kết nối MongoDB
from app.routes.dependencies import get_current_user
from app.services.analysis_service import (
    DATABASE_ERRORS,
    LEGACY_ROLE_ID_ALIASES,
    get_analysis_detail,
    get_role_by_id,
    list_career_roles,
)

router = APIRouter(prefix="/api/v1/analyses", tags=["Analysis"])

@router.get("", summary="UC-024: Xem lịch sử phân tích")
async def get_analysis_history(
    user: dict = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=50)
):
    user_id = user["user_id"]
    
    # Sử dụng Aggregation Pipeline của MongoDB để JOIN bảng KETQUA_PTCV và bảng CV
    pipeline = [
        {
            "$lookup": {
                "from": "CV",
                "localField": "MaCV",
                "foreignField": "_id",
                "as": "cv_info"
            }
        },
        # Chuyển mảng cv_info thành object
        {"$unwind": "$cv_info"},

        {
            "$lookup": {
                "from": "NGANHNGHIET",
                "localField": "MaNganh",
                "foreignField": "_id",
                "as": "role_info"
            }
        },
        {"$unwind": {"path": "$role_info", "preserveNullAndEmptyArrays": True}},
        
        # Chỉ lấy CV của user hiện tại đang đăng nhập
        {"$match": {"cv_info.MaKH": user_id}},
        
        # Sắp xếp mới nhất lên đầu
        {"$sort": {"ThoiDiemPT": -1}},
        
        # Format lại dữ liệu trả về cho Frontend
        {
            "$project": {
                "_id": 0,
                "analysis_id": "$_id",
                "cv_name": "$cv_info.TenFileGoc",
                "overall_score": "$DiemTongQuan",
                "classification": "$XepLoai",
                "role_id": {"$ifNull": ["$MaNganh", "$cv_info.MaNganh"]},
                "role_name": "$role_info.TenNganh",
                "created_at": "$ThoiDiemPT",
                "status": "$cv_info.TrangThai"
            }
        }
    ]
    
    # Thực thi truy vấn với AsyncIOMotorClient
    try:
        cursor = db["KETQUA_PTCV"].aggregate(pipeline)
        history_list = await cursor.to_list(length=limit)
    except DATABASE_ERRORS:
        return {
            "data": [],
            "access_level": user["current_plan"],
            "meta": {
                "visible_count": 0,
                "locked_count": 0,
                "free_history_limit": 3
            },
            "message": "Chưa kết nối được cơ sở dữ liệu lịch sử phân tích."
        }
    
    # Format datetime object sang ISO string cho JSON response
    for item in history_list:
        if hasattr(item["created_at"], "isoformat"):
            item["created_at"] = item["created_at"].isoformat()

    if any(not item.get("role_name") and item.get("role_id") for item in history_list):
        roles = await list_career_roles(db)
        role_name_by_id = {role["role_id"]: role["name"] for role in roles}
        for item in history_list:
            if not item.get("role_name") and item.get("role_id"):
                resolved_role_id = LEGACY_ROLE_ID_ALIASES.get(item["role_id"], item["role_id"])
                item["role_name"] = role_name_by_id.get(resolved_role_id)

    # BR2: Registered User chỉ xem được số lượng kết quả giới hạn (Ví dụ: 3 CV gần nhất)
    if user["current_plan"] != "premium":
        return {
            "data": history_list[:3],
            "access_level": "free",
            "meta": {
                "visible_count": min(len(history_list), 3),
                "locked_count": max(0, len(history_list) - 3),
                "free_history_limit": 3
            },
            "message": "Nâng cấp Premium để xem toàn bộ lịch sử."
        }
    
    return {
        "data": history_list,
        "access_level": "premium",
        "meta": {
            "visible_count": len(history_list),
            "locked_count": 0,
            "free_history_limit": 3
        }
    }

@router.get("/{analysis_id}", summary="UC-015: Xem điểm tổng quan, điểm thành phần và lỗi cơ bản")
async def get_analysis_result(analysis_id: str, user: dict = Depends(get_current_user)):
    detail = await get_analysis_detail(
        db=db,
        analysis_id=analysis_id,
        user_id=user["user_id"],
    )
    if not detail.get("role_name") and detail.get("role_id"):
        try:
            role = await get_role_by_id(db, detail["role_id"])
            detail["role_name"] = role["name"]
            detail["role_description"] = role["description"]
        except HTTPException:
            pass
    return {"data": detail, "access_level": user["current_plan"], "error": None}

@router.get("/{analysis_id}/suggestions", summary="UC-016: Xem gợi ý cải thiện CV")
async def get_suggestions(analysis_id: str, user: dict = Depends(get_current_user)):
    # Truy xuất trực tiếp các gợi ý từ collection GOIY_CAITHIEN
    cursor = db["GOIY_CAITHIEN"].find({"MaKQ": analysis_id}).sort("DoUuTien", 1)
    suggestions_from_db = await cursor.to_list(length=100)
    
    if not suggestions_from_db:
        raise HTTPException(status_code=404, detail="Không tìm thấy gợi ý nào cho kết quả này.")

    formatted_suggestions = []
    for sug in suggestions_from_db:
        formatted_sug = {
            "suggestion_id": sug["_id"],
            "category": sug.get("Loai", "Nội dung"),
            "issue": sug.get("MoTaVanDe", ""),
            "basic_fix": sug.get("GiaiPhap", ""),
            # Nếu database chưa seed trường example_rewrite, mình fallback một chuỗi mặc định
            "premium_rewrite": sug.get("example_rewrite", "Đây là câu mẫu VIP từ AI (Chuẩn STAR)..."), 
            "is_premium": sug.get("is_premium", False)
        }
        
        # Ràng buộc phân quyền nội dung: khóa premium_rewrite nếu user đang dùng gói Free
        if formatted_sug["is_premium"] and user["current_plan"] != "premium":
            formatted_sug["premium_rewrite"] = "Tính năng khóa. Vui lòng nâng cấp Premium để xem câu mẫu chuẩn ATS."
            
        formatted_suggestions.append(formatted_sug)

    return {"data": formatted_suggestions, "access_level": user["current_plan"]}
