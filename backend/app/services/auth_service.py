"""Authentication service for UC-008, UC-009, and UC-010."""

from __future__ import annotations

import base64
import hashlib
import hmac
import os
import re
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import uuid4

import jwt
from fastapi import HTTPException, status

from app.services.analysis_service import DATABASE_ERRORS


JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "smartcv-local-dev-change-me")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_MINUTES = int(os.getenv("ACCESS_TOKEN_MINUTES", "30"))
REFRESH_TOKEN_DAYS = int(os.getenv("REFRESH_TOKEN_DAYS", "7"))
REMEMBER_ME_REFRESH_DAYS = int(os.getenv("REMEMBER_ME_REFRESH_DAYS", "30"))
TEMP_LOCK_MINUTES = int(os.getenv("AUTH_TEMP_LOCK_MINUTES", "15"))
MAX_FAILED_LOGIN_ATTEMPTS = int(os.getenv("AUTH_MAX_FAILED_LOGIN_ATTEMPTS", "5"))
PASSWORD_RESET_TOKEN_MINUTES = int(os.getenv("PASSWORD_RESET_TOKEN_MINUTES", "30"))
PASSWORD_HASH_PREFIX = "scrypt"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def normalize_email(email: str) -> str:
    return email.strip().lower()


def is_valid_email(email: str) -> bool:
    return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email.strip()) is not None


def validate_password_strength(password: str) -> None:
    has_letter = re.search(r"[A-Za-zÀ-ỹ]", password) is not None
    has_digit = re.search(r"\d", password) is not None
    if len(password) < 8 or not has_letter or not has_digit:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "AUTH_PASSWORD_WEAK",
                "message": "Mật khẩu phải có tối thiểu 8 ký tự, bao gồm chữ và số.",
            },
        )


def mask_email(email: str) -> str:
    local, _, domain = email.partition("@")
    if not local or not domain:
        return email
    visible = local[0]
    return f"{visible}{'*' * max(2, len(local) - 1)}@{domain}"


def token_hash(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    key = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1, dklen=32)
    return "$".join(
        [
            PASSWORD_HASH_PREFIX,
            "16384",
            "8",
            "1",
            base64.urlsafe_b64encode(salt).decode("ascii"),
            base64.urlsafe_b64encode(key).decode("ascii"),
        ]
    )


def verify_password(password: str, stored_hash: str | None) -> bool:
    if not stored_hash or not stored_hash.startswith(f"{PASSWORD_HASH_PREFIX}$"):
        return False

    try:
        _, n_value, r_value, p_value, salt_value, hash_value = stored_hash.split("$", 5)
        salt = base64.urlsafe_b64decode(salt_value.encode("ascii"))
        expected = base64.urlsafe_b64decode(hash_value.encode("ascii"))
        actual = hashlib.scrypt(
            password.encode("utf-8"),
            salt=salt,
            n=int(n_value),
            r=int(r_value),
            p=int(p_value),
            dklen=len(expected),
        )
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def account_query_by_email(email: str) -> dict[str, Any]:
    normalized = normalize_email(email)
    return {
        "$or": [
            {"EmailNormalized": normalized},
            {"Email": {"$regex": f"^{re.escape(normalized)}$", "$options": "i"}},
        ]
    }


def public_user(customer: dict[str, Any] | None, account: dict[str, Any]) -> dict[str, Any]:
    role = account.get("Role") or ("admin" if account.get("MaADM") else "registered")
    plan = "admin" if role == "admin" else str((customer or {}).get("LoaiKH", "registered")).lower()
    return {
        "user_id": account.get("MaKH") or account.get("MaADM"),
        "account_id": account.get("_id"),
        "full_name": (customer or {}).get("HoTen") or account.get("HoTen") or account.get("Email"),
        "email": account.get("Email"),
        "role": role,
        "account_type": plan,
        "status": account.get("TrangThai", "active"),
        "email_verified": bool(account.get("EmailVerified", role == "admin")),
    }


async def find_account_by_email(db: Any, email: str) -> dict[str, Any] | None:
    return await db["TAIKHOAN"].find_one(account_query_by_email(email))


async def find_customer_for_account(db: Any, account: dict[str, Any]) -> dict[str, Any] | None:
    if account.get("MaKH"):
        return await db["KHACHHANG"].find_one({"_id": account["MaKH"]})
    if account.get("MaADM"):
        return await db["ADMIN"].find_one({"_id": account["MaADM"]})
    return None


def issue_access_token(account: dict[str, Any]) -> tuple[str, datetime]:
    expires_at = utc_now() + timedelta(minutes=ACCESS_TOKEN_MINUTES)
    payload = {
        "sub": account["_id"],
        "user_id": account.get("MaKH") or account.get("MaADM"),
        "role": account.get("Role") or ("admin" if account.get("MaADM") else "registered"),
        "type": "access",
        "exp": expires_at,
        "iat": utc_now(),
        "jti": uuid4().hex,
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM), expires_at


async def issue_refresh_token(db: Any, account: dict[str, Any], remember_me: bool) -> tuple[str, datetime]:
    token = secrets.token_urlsafe(48)
    expires_at = utc_now() + timedelta(days=REMEMBER_ME_REFRESH_DAYS if remember_me else REFRESH_TOKEN_DAYS)
    await db["REFRESH_TOKENS"].insert_one(
        {
            "_id": f"RT_{uuid4().hex[:16].upper()}",
            "TokenHash": token_hash(token),
            "MaTK": account["_id"],
            "MaKH": account.get("MaKH"),
            "MaADM": account.get("MaADM"),
            "CreatedAt": utc_now(),
            "ExpiresAt": expires_at,
            "RevokedAt": None,
            "RememberMe": remember_me,
        }
    )
    return token, expires_at


async def build_session_response(db: Any, account: dict[str, Any], remember_me: bool) -> dict[str, Any]:
    customer = await find_customer_for_account(db, account)
    access_token, access_expires_at = issue_access_token(account)
    refresh_token, refresh_expires_at = await issue_refresh_token(db, account, remember_me)
    return {
        "user": public_user(customer, account),
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_at": access_expires_at,
        "refresh_expires_at": refresh_expires_at,
    }


def ensure_account_can_login(account: dict[str, Any]) -> None:
    locked_until = account.get("LockedUntil")
    if isinstance(locked_until, datetime) and locked_until > utc_now():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "AUTH_ACCOUNT_TEMP_LOCKED",
                "message": "Tài khoản của bạn đã bị tạm khóa.",
                "locked_until": locked_until,
            },
        )

    status_value = str(account.get("TrangThai", "active")).lower()
    if status_value in {"locked", "khoa", "khóa", "da_khoa", "đã khóa"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "AUTH_ACCOUNT_LOCKED", "message": "Tài khoản của bạn đã bị tạm khóa."},
        )


async def register_user(
    db: Any,
    *,
    full_name: str,
    email: str,
    password: str,
    password_confirmation: str,
    terms_accepted: bool,
) -> dict[str, Any]:
    normalized_email = normalize_email(email)
    clean_name = full_name.strip()

    if not clean_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "AUTH_REQUIRED_FIELD", "message": "Vui lòng nhập đầy đủ thông tin bắt buộc."},
        )
    if not is_valid_email(normalized_email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "AUTH_EMAIL_INVALID", "message": "Email không đúng định dạng."},
        )
    if password != password_confirmation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "AUTH_PASSWORD_MISMATCH", "message": "Mật khẩu xác nhận không khớp."},
        )
    if not terms_accepted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "AUTH_TERMS_REQUIRED", "message": "Bạn cần đồng ý với điều khoản để đăng ký."},
        )
    validate_password_strength(password)

    try:
        existing_account = await find_account_by_email(db, normalized_email)
        if existing_account:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"code": "AUTH_EMAIL_EXISTS", "message": "Email này đã được sử dụng."},
            )

        now = utc_now()
        customer_id = f"KH_{uuid4().hex[:10].upper()}"
        account_id = f"TK_{customer_id}"

        customer = {
            "_id": customer_id,
            "HoTen": clean_name,
            "Email": normalized_email,
            "EmailNormalized": normalized_email,
            "TrangThai": "Hoạt động",
            "LoaiKH": "registered",
            "TrinhDoHV": "",
            "ViTriNN": "",
            "NNQuanTam": "",
            "AvatarUrl": None,
            "NgayDangKy": now,
            "NgayCapNhat": now,
        }
        account = {
            "_id": account_id,
            "Email": normalized_email,
            "EmailNormalized": normalized_email,
            "MatKhauHash": hash_password(password),
            "MaKH": customer_id,
            "Role": "registered",
            "TrangThai": "active",
            "EmailVerified": True,
            "VerifiedAt": now,
            "FailedLoginCount": 0,
            "LockedUntil": None,
            "CreatedAt": now,
            "UpdatedAt": now,
        }

        await db["KHACHHANG"].insert_one(customer)
        await db["TAIKHOAN"].insert_one(account)
        await db["LOG_KH"].insert_one(
            {
                "_id": f"LOG_{account_id}_{uuid4().hex[:8].upper()}",
                "HanhDong": "Đăng ký tài khoản",
                "DuLieuTruoc": None,
                "DuLieuSau": {"Email": normalized_email, "TrangThai": "active"},
                "KetQua": "Thanh cong",
                "ThoiDiemThucHien": now,
                "MaKH": customer_id,
                "DoiTuong": "TAIKHOAN",
                "MaDoiTuong": account_id,
            }
        )
    except HTTPException:
        raise
    except DATABASE_ERRORS as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"code": "DATABASE_UNAVAILABLE", "message": "Chưa tạo được tài khoản vì MongoDB chưa sẵn sàng."},
        ) from exc

    return {
        "user": public_user(customer, account),
    }


async def login_user(db: Any, *, email: str, password: str, remember_me: bool) -> dict[str, Any]:
    normalized_email = normalize_email(email)
    if not is_valid_email(normalized_email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "AUTH_EMAIL_INVALID", "message": "Email không đúng định dạng."},
        )

    try:
        account = await find_account_by_email(db, normalized_email)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"code": "AUTH_INVALID_CREDENTIALS", "message": "Thông tin đăng nhập không chính xác."},
            )

        ensure_account_can_login(account)
        stored_hash = account.get("MatKhauHash") or account.get("Matkhau")
        if not verify_password(password, stored_hash):
            failed_count = int(account.get("FailedLoginCount", 0) or 0) + 1
            updates: dict[str, Any] = {"FailedLoginCount": failed_count, "UpdatedAt": utc_now()}
            if failed_count >= MAX_FAILED_LOGIN_ATTEMPTS:
                updates["LockedUntil"] = utc_now() + timedelta(minutes=TEMP_LOCK_MINUTES)
            await db["TAIKHOAN"].update_one({"_id": account["_id"]}, {"$set": updates})
            if failed_count >= MAX_FAILED_LOGIN_ATTEMPTS:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail={
                        "code": "AUTH_ACCOUNT_TEMP_LOCKED",
                        "message": "Tài khoản của bạn đã bị tạm khóa.",
                        "attempts": failed_count,
                    },
                )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "code": "AUTH_INVALID_CREDENTIALS",
                    "message": "Thông tin đăng nhập không chính xác.",
                    "attempts_remaining": max(0, MAX_FAILED_LOGIN_ATTEMPTS - failed_count),
                },
            )

        now = utc_now()
        login_updates: dict[str, Any] = {"FailedLoginCount": 0, "LockedUntil": None, "LastLoginAt": now, "UpdatedAt": now}
        if not account.get("EmailVerified"):
            login_updates.update({"EmailVerified": True, "VerifiedAt": now, "TrangThai": "active"})
        await db["TAIKHOAN"].update_one(
            {"_id": account["_id"]},
            {"$set": login_updates},
        )
        if account.get("MaKH"):
            await db["KHACHHANG"].update_one(
                {"_id": account["MaKH"]},
                {"$set": {"LanDangNhapCuoi": now, "TrangThai": "Hoạt động"}},
            )

        fresh_account = await db["TAIKHOAN"].find_one({"_id": account["_id"]}) or account
        return await build_session_response(db, fresh_account, remember_me)
    except HTTPException:
        raise
    except DATABASE_ERRORS as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"code": "DATABASE_UNAVAILABLE", "message": "Chưa đăng nhập được vì MongoDB chưa sẵn sàng."},
        ) from exc


async def refresh_session(db: Any, refresh_token: str) -> dict[str, Any]:
    digest = token_hash(refresh_token)
    try:
        token_doc = await db["REFRESH_TOKENS"].find_one(
            {"TokenHash": digest, "RevokedAt": None, "ExpiresAt": {"$gt": utc_now()}}
        )
        if not token_doc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"code": "AUTH_REFRESH_INVALID", "message": "Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại."},
            )

        account = await db["TAIKHOAN"].find_one({"_id": token_doc["MaTK"]})
        if not account:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"code": "AUTH_REFRESH_INVALID", "message": "Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại."},
            )
        ensure_account_can_login(account)

        await db["REFRESH_TOKENS"].update_one({"_id": token_doc["_id"]}, {"$set": {"RevokedAt": utc_now()}})
        return await build_session_response(db, account, bool(token_doc.get("RememberMe")))
    except HTTPException:
        raise
    except DATABASE_ERRORS as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"code": "DATABASE_UNAVAILABLE", "message": "Chưa làm mới phiên vì MongoDB chưa sẵn sàng."},
        ) from exc


async def logout_user(db: Any, refresh_token: str | None) -> dict[str, str]:
    if refresh_token:
        try:
            await db["REFRESH_TOKENS"].update_many(
                {"TokenHash": token_hash(refresh_token), "RevokedAt": None},
                {"$set": {"RevokedAt": utc_now()}},
            )
        except DATABASE_ERRORS as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail={"code": "DATABASE_UNAVAILABLE", "message": "Chưa đăng xuất được vì MongoDB chưa sẵn sàng."},
            ) from exc
    return {"message": "Đăng xuất thành công."}


async def forgot_password(db: Any, email: str) -> dict[str, Any]:
    normalized_email = normalize_email(email)
    if not is_valid_email(normalized_email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "AUTH_EMAIL_INVALID", "message": "Email không đúng định dạng."},
        )

    try:
        account = await find_account_by_email(db, normalized_email)
        reset_token = secrets.token_urlsafe(32)
        expires_at = utc_now() + timedelta(minutes=PASSWORD_RESET_TOKEN_MINUTES)
        if account:
            await db["TAIKHOAN"].update_one(
                {"_id": account["_id"]},
                {
                    "$set": {
                        "PasswordResetTokenHash": token_hash(reset_token),
                        "PasswordResetExpiresAt": expires_at,
                        "UpdatedAt": utc_now(),
                    }
                },
            )
    except DATABASE_ERRORS as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"code": "DATABASE_UNAVAILABLE", "message": "Chưa gửi được liên kết đặt lại mật khẩu vì MongoDB chưa sẵn sàng."},
        ) from exc

    return {
        "message": "Liên kết đặt lại mật khẩu đã được gửi. Vui lòng kiểm tra email.",
        "email_masked": mask_email(normalized_email),
        "delivery": "mock_email_queued",
        "demo_reset_token": reset_token if account else None,
        "expires_at": expires_at,
    }


async def reset_password(
    db: Any,
    *,
    token: str,
    password: str,
    password_confirmation: str,
) -> dict[str, str]:
    if password != password_confirmation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "AUTH_PASSWORD_MISMATCH", "message": "Mật khẩu xác nhận không khớp."},
        )
    validate_password_strength(password)

    try:
        account = await db["TAIKHOAN"].find_one({"PasswordResetTokenHash": token_hash(token)})
        if not account:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": "AUTH_RESET_INVALID", "message": "Liên kết đặt lại mật khẩu không hợp lệ hoặc đã hết hạn."},
            )
        expires_at = account.get("PasswordResetExpiresAt")
        if isinstance(expires_at, datetime) and expires_at < utc_now():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": "AUTH_RESET_EXPIRED", "message": "Liên kết đặt lại mật khẩu không hợp lệ hoặc đã hết hạn."},
            )

        await db["TAIKHOAN"].update_one(
            {"_id": account["_id"]},
            {
                "$set": {"MatKhauHash": hash_password(password), "FailedLoginCount": 0, "LockedUntil": None, "UpdatedAt": utc_now()},
                "$unset": {"PasswordResetTokenHash": "", "PasswordResetExpiresAt": ""},
            },
        )
    except HTTPException:
        raise
    except DATABASE_ERRORS as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"code": "DATABASE_UNAVAILABLE", "message": "Chưa đặt lại được mật khẩu vì MongoDB chưa sẵn sàng."},
        ) from exc

    return {"message": "Cập nhật mật khẩu thành công."}


async def get_current_user_from_token(db: Any, token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        if payload.get("type") != "access":
            raise jwt.InvalidTokenError("Invalid token type")
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "AUTH_SESSION_EXPIRED", "message": "Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại."},
        ) from exc
    except jwt.InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "AUTH_TOKEN_INVALID", "message": "Phiên đăng nhập không hợp lệ."},
        ) from exc

    account_id = payload.get("sub")
    try:
        account = await db["TAIKHOAN"].find_one({"_id": account_id})
        if not account:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"code": "AUTH_TOKEN_INVALID", "message": "Phiên đăng nhập không hợp lệ."},
            )
        ensure_account_can_login(account)
        customer = await find_customer_for_account(db, account)
    except HTTPException:
        raise
    except DATABASE_ERRORS as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"code": "DATABASE_UNAVAILABLE", "message": "Chưa xác thực được phiên vì MongoDB chưa sẵn sàng."},
        ) from exc

    public = public_user(customer, account)
    return {
        "user_id": public["user_id"],
        "account_id": public["account_id"],
        "role": public["role"],
        "current_plan": public["account_type"],
        "email": public["email"],
        "full_name": public["full_name"],
    }
