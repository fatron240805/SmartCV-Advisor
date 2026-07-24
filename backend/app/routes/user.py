"""Routes for user profile and privacy settings."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.db import db
from app.routes.dependencies import get_current_user
from app.services.analysis_service import DATABASE_ERRORS, resolve_quota_state
from app.services.user_service import get_profile, request_data_deletion, update_profile

VALID_PLAN_IDS = {"DV_FREE", "DV_PREMIUM_30", "DV_PREMIUM_90"}
PREMIUM_PLAN_IDS = {"DV_PREMIUM_30", "DV_PREMIUM_90"}


router = APIRouter(prefix="/api/v1/users", tags=["User Profile"])


class ProfileUpdateRequest(BaseModel):
    full_name: str | None = Field(default=None, max_length=120)
    email: str | None = Field(default=None, max_length=254)
    industry_interest: str | None = Field(default=None, max_length=160)
    target_role: str | None = Field(default=None, max_length=160)
    current_level: str | None = Field(default=None, max_length=160)
    avatar_url: str | None = None


class DataDeletionRequest(BaseModel):
    scope: str = Field(default="cv_data")
    reason: str | None = Field(default=None, max_length=500)


@router.get("/me", summary="UC-011: Xem thông tin cá nhân")
async def get_me(user: dict[str, str] = Depends(get_current_user)) -> dict[str, Any]:
    profile = await get_profile(db, user["user_id"])
    return {"data": profile, "error": None}


@router.patch("/me", summary="UC-011: Cập nhật thông tin cá nhân")
async def update_me(
    payload: ProfileUpdateRequest,
    user: dict[str, str] = Depends(get_current_user),
) -> dict[str, Any]:
    profile = await update_profile(
        db,
        user_id=user["user_id"],
        full_name=payload.full_name,
        email=payload.email,
        industry_interest=payload.industry_interest,
        target_role=payload.target_role,
        current_level=payload.current_level,
        avatar_url=payload.avatar_url,
    )
    return {
        "data": profile,
        "meta": {"message": "Cập nhật thông tin cá nhân thành công."},
        "error": None,
    }


@router.post("/me/data-deletion-request", summary="UC-011: Yêu cầu xóa dữ liệu")
async def create_data_deletion_request(
    payload: DataDeletionRequest,
    user: dict[str, str] = Depends(get_current_user),
) -> dict[str, Any]:
    deletion_request = await request_data_deletion(
        db,
        user_id=user["user_id"],
        scope=payload.scope,
        reason=payload.reason,
    )
    return {
        "data": deletion_request,
        "meta": {"message": "Yêu cầu xóa dữ liệu đã được ghi nhận."},
        "error": None,
    }


@router.get("/me/quota", summary="Lấy lượt phân tích còn lại trong chu kỳ hiện tại")
async def get_my_quota(user: dict[str, str] = Depends(get_current_user)) -> dict[str, Any]:
    """Trả về số lượt đã dùng và còn lại.
    Premium: unlimited=True. Registered: used/limit/remaining."""
    from datetime import datetime, timezone

    user_id = user["user_id"]

    try:
        now = datetime.now(timezone.utc)
        # Dùng chung logic xác định gói/limit/period_start với bước chặn
        # upload CV và chặn tạo phân tích (app.services.analysis_service).
        state = await resolve_quota_state(db, user_id, now)

        account_type = state["account_type"]
        current_plan_id = state["plan_id"]
        limit = state["limit"]
        is_unlimited = state["is_unlimited"]
        period_start = state["period_start"]

        # Đếm TỔNG số lần phân tích để HIỂN THỊ (không lọc ngày)
        used = await db["LICHSUPTCV"].count_documents({"MaKH": user_id})

        # Tính số lượt còn lại theo chu kỳ hiện tại (có lọc theo period_start)
        if not is_unlimited:
            used_in_period = await db["LICHSUPTCV"].count_documents({
                "MaKH": user_id,
                "NgayPT": {"$gte": period_start}
            })
            remaining = max(0, limit - used_in_period)
        else:
            remaining = None

        label = "Không giới hạn" if is_unlimited else f"{remaining}/{limit} lượt còn lại"

        return {
            "data": {
                "account_type": account_type,
                "current_plan_id": current_plan_id,
                "unlimited": is_unlimited,
                "used": used,
                "limit": None if is_unlimited else limit,
                "remaining": remaining,
                "label": label,
            },
            "error": None,
        }
    except DATABASE_ERRORS:
        return {
            "data": {
                "account_type": "registered",
                "current_plan_id": "DV_FREE",
                "unlimited": False,
                "used": 0,
                "limit": 3,
                "remaining": 3,
                "label": "3/3 lượt còn lại",
            },
            "error": None,
        }


@router.post("/me/change-plan", summary="Nâng cấp hoặc thay đổi gói dịch vụ")
async def change_plan(
    payload: dict,
    user: dict[str, str] = Depends(get_current_user),
) -> dict[str, Any]:
    """Nâng cấp registered → premium hoặc từ premium 30 → premium 90.
    Cập nhật LoaiKH trong KHACHHANG và tạo/cập nhật LUOTDUNG."""
    from datetime import datetime, timezone, timedelta
    from uuid import uuid4
    from fastapi import HTTPException

    user_id = user["user_id"]
    new_plan_id = str(payload.get("plan_id", "")).strip()

    if new_plan_id not in VALID_PLAN_IDS:
        raise HTTPException(status_code=400, detail={"code": "INVALID_PLAN", "message": "Gói dịch vụ không hợp lệ."})

    now = datetime.now(timezone.utc)
    plan_to_loai = {
        "DV_FREE": "registered",
        "DV_PREMIUM_30": "premium",
        "DV_PREMIUM_90": "premium",
    }
    plan_to_days = {"DV_PREMIUM_30": 30, "DV_PREMIUM_90": 90}
    new_loai_kh = plan_to_loai[new_plan_id]
    duration_days = plan_to_days.get(new_plan_id)

    # Cập nhật loại tài khoản
    await db["KHACHHANG"].update_one({"_id": user_id}, {"$set": {"LoaiKH": new_loai_kh}})
    await db["TAIKHOAN"].update_one(
        {"MaKH": user_id},
        {"$set": {"Role": new_loai_kh, "UpdatedAt": now}},
    )

    if new_plan_id in PREMIUM_PLAN_IDS and duration_days:
        # Tạo/cập nhật LUOTDUNG với gói mới
        await db["LUOTDUNG"].update_one(
            {"MaKH": user_id, "MaGoiDV": new_plan_id},
            {
                "$set": {
                    "MaKH": user_id,
                    "MaGoiDV": new_plan_id,
                    "NgayBatDau": now,
                    "HanSuDung": now + timedelta(days=duration_days),
                },
                "$setOnInsert": {"_id": f"LD_{uuid4().hex[:10].upper()}"},
            },
            upsert=True,
        )

    return {
        "data": {"plan_id": new_plan_id, "account_type": new_loai_kh},
        "meta": {"message": "Nâng cấp gói dịch vụ thành công."},
        "error": None,
    }


@router.post("/me/renew-plan", summary="Gia hạn gói hiện tại")
async def renew_plan(
    user: dict[str, str] = Depends(get_current_user),
) -> dict[str, Any]:
    """Gia hạn gói premium hiện tại thêm số ngày tương ứng."""
    from datetime import datetime, timezone, timedelta
    from fastapi import HTTPException

    user_id = user["user_id"]
    now = datetime.now(timezone.utc)

    usage_doc = await db["LUOTDUNG"].find_one({"MaKH": user_id}, sort=[("HanSuDung", -1)])
    if not usage_doc or usage_doc.get("MaGoiDV") not in PREMIUM_PLAN_IDS:
        raise HTTPException(status_code=400, detail={"code": "NOT_PREMIUM", "message": "Chỉ gói Premium mới có thể gia hạn."})

    plan_id = usage_doc["MaGoiDV"]
    plan_to_days = {"DV_PREMIUM_30": 30, "DV_PREMIUM_90": 90}
    duration_days = plan_to_days.get(plan_id, 30)

    # Gia hạn: nếu còn hạn thì cộng thêm từ HanSuDung, nếu hết hạn thì tính từ now
    current_expiry = usage_doc.get("HanSuDung")
    if current_expiry:
        current_naive = current_expiry.replace(tzinfo=None)
        now_naive = now.replace(tzinfo=None)
        base = current_naive if current_naive > now_naive else now_naive
    else:
        base = now.replace(tzinfo=None)

    new_expiry = base.replace(tzinfo=timezone.utc) + timedelta(days=duration_days)

    await db["LUOTDUNG"].update_one(
        {"_id": usage_doc["_id"]},
        {"$set": {"HanSuDung": new_expiry}},
    )

    return {
        "data": {"plan_id": plan_id, "new_expiry": new_expiry.isoformat()},
        "meta": {"message": f"Gia hạn gói {duration_days} ngày thành công."},
        "error": None,
    }


@router.post("/me/cancel-plan", summary="Hủy gói Premium, về lại Free")
async def cancel_plan(
    user: dict[str, str] = Depends(get_current_user),
) -> dict[str, Any]:
    """Hủy gói premium, đưa tài khoản về registered (free)."""
    from datetime import datetime, timezone
    from fastapi import HTTPException

    user_id = user["user_id"]
    now = datetime.now(timezone.utc)

    customer = await db["KHACHHANG"].find_one({"_id": user_id})
    if not customer or customer.get("LoaiKH") != "premium":
        raise HTTPException(status_code=400, detail={"code": "NOT_PREMIUM", "message": "Tài khoản hiện không phải Premium."})

    # Đưa về registered
    await db["KHACHHANG"].update_one({"_id": user_id}, {"$set": {"LoaiKH": "registered"}})
    await db["TAIKHOAN"].update_one(
        {"MaKH": user_id},
        {"$set": {"Role": "registered", "UpdatedAt": now}},
    )
    # Hủy LUOTDUNG premium (set HanSuDung về quá khứ)
    await db["LUOTDUNG"].update_many(
        {"MaKH": user_id, "MaGoiDV": {"$in": list(PREMIUM_PLAN_IDS)}},
        {"$set": {"HanSuDung": now}},
    )

    return {
        "data": {"account_type": "registered"},
        "meta": {"message": "Đã hủy gói Premium. Tài khoản về gói Free."},
        "error": None,
    }
