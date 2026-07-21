"""Routes for authentication and user sessions."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, status
from pydantic import BaseModel, Field

from app.db import db
from app.services.auth_service import (
    forgot_password,
    login_user,
    logout_user,
    refresh_session,
    register_user,
    resend_verification_email,
    reset_password,
    verify_email,
)


router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


class RegisterRequest(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=120)
    email: str = Field(..., min_length=5, max_length=254)
    password: str = Field(..., min_length=8, max_length=128)
    password_confirmation: str = Field(..., min_length=8, max_length=128)
    terms_accepted: bool


class VerifyEmailRequest(BaseModel):
    token: str = Field(..., min_length=8)


class ResendVerificationRequest(BaseModel):
    email: str = Field(..., min_length=5, max_length=254)


class LoginRequest(BaseModel):
    email: str = Field(..., min_length=5, max_length=254)
    password: str = Field(..., min_length=1, max_length=128)
    remember_me: bool = False


class RefreshRequest(BaseModel):
    refresh_token: str = Field(..., min_length=8)


class LogoutRequest(BaseModel):
    refresh_token: str | None = None


class ForgotPasswordRequest(BaseModel):
    email: str = Field(..., min_length=5, max_length=254)


class ResetPasswordRequest(BaseModel):
    token: str = Field(..., min_length=8)
    password: str = Field(..., min_length=8, max_length=128)
    password_confirmation: str = Field(..., min_length=8, max_length=128)


@router.post("/register", status_code=status.HTTP_201_CREATED, summary="UC-008: Đăng ký tài khoản")
async def register(payload: RegisterRequest) -> dict[str, Any]:
    result = await register_user(
        db,
        full_name=payload.full_name,
        email=payload.email,
        password=payload.password,
        password_confirmation=payload.password_confirmation,
        terms_accepted=payload.terms_accepted,
    )
    return {
        "data": result["user"],
        "meta": {
            "next_step": "verify_email",
            "verification": result["verification"],
        },
        "error": None,
    }


@router.post("/verify-email", summary="UC-008: Xác thực email")
async def verify_email_route(payload: VerifyEmailRequest) -> dict[str, Any]:
    result = await verify_email(db, payload.token)
    return {
        "data": result["user"],
        "meta": {"next_step": "login"},
        "error": None,
    }


@router.post("/resend-verification", summary="UC-008: Gửi lại email xác thực")
async def resend_verification(payload: ResendVerificationRequest) -> dict[str, Any]:
    result = await resend_verification_email(db, payload.email)
    return {
        "data": result,
        "meta": {"next_step": "verify_email"},
        "error": None,
    }


@router.post("/login", summary="UC-009: Đăng nhập")
async def login(payload: LoginRequest) -> dict[str, Any]:
    result = await login_user(
        db,
        email=payload.email,
        password=payload.password,
        remember_me=payload.remember_me,
    )
    return {
        "data": result,
        "meta": {"next_step": "dashboard"},
        "error": None,
    }


@router.post("/refresh", summary="UC-009: Làm mới phiên đăng nhập")
async def refresh(payload: RefreshRequest) -> dict[str, Any]:
    result = await refresh_session(db, payload.refresh_token)
    return {"data": result, "meta": {"next_step": "continue"}, "error": None}


@router.post("/logout", summary="UC-010: Đăng xuất")
async def logout(payload: LogoutRequest) -> dict[str, Any]:
    result = await logout_user(db, payload.refresh_token)
    return {"data": result, "meta": {"next_step": "login"}, "error": None}


@router.post("/forgot-password", summary="UC-009: Quên mật khẩu")
async def forgot_password_route(payload: ForgotPasswordRequest) -> dict[str, Any]:
    result = await forgot_password(db, payload.email)
    return {"data": result, "meta": {"next_step": "reset_password"}, "error": None}


@router.post("/reset-password", summary="UC-009: Tạo mật khẩu mới")
async def reset_password_route(payload: ResetPasswordRequest) -> dict[str, Any]:
    result = await reset_password(
        db,
        token=payload.token,
        password=payload.password,
        password_confirmation=payload.password_confirmation,
    )
    return {"data": result, "meta": {"next_step": "login"}, "error": None}
