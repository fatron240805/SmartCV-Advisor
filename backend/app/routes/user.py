"""Routes for user profile and privacy settings."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.db import db
from app.routes.dependencies import get_current_user
from app.services.analysis_service import DATABASE_ERRORS, resolve_quota_state
from app.services.user_service import get_profile, request_data_deletion, update_profile


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
