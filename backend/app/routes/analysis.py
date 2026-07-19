"""Routes for CV analysis and JD matching."""

# Định nghĩa route cho phân tích, so sánh kỹ năng và kết quả.

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any
from app.db import db  # Import instance kết nối MongoDB

router = APIRouter(prefix="/api/v1/analyses", tags=["Analysis"])

# Mock Dependency lấy user hiện tại (sau này ông Auth sẽ viết hàm decode JWT thay vào đây)
async def get_current_user():
    # Giả lập user KH001 (đã có trong file create_collections.py) đang dùng gói Free
    return {"user_id": "KH001", "current_plan": "free"}

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
                "created_at": "$ThoiDiemPT",
                "status": "$cv_info.TrangThai"
            }
        }
    ]
    
    # Thực thi truy vấn với AsyncIOMotorClient
    cursor = db["KETQUA_PTCV"].aggregate(pipeline)
    history_list = await cursor.to_list(length=limit)
    
    # Format datetime object sang ISO string cho JSON response
    for item in history_list:
        if hasattr(item["created_at"], "isoformat"):
            item["created_at"] = item["created_at"].isoformat()

    # BR2: Registered User chỉ xem được số lượng kết quả giới hạn (Ví dụ: 3 CV gần nhất)
    if user["current_plan"] != "premium":
        return {
            "data": history_list[:3],
            "access_level": "free",
            "message": "Nâng cấp Premium để xem toàn bộ lịch sử."
        }
    
    return {
        "data": history_list,
        "access_level": "premium"
    }

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
