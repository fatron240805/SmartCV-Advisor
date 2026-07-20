"""Routes for user profile and privacy settings."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.db import db
from app.routes.dependencies import get_current_user
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
