"""Shared FastAPI dependencies for request context."""

from __future__ import annotations

from fastapi import Header

from app.db import db
from app.services.auth_service import get_current_user_from_token


async def get_current_user(authorization: str | None = Header(default=None)) -> dict[str, str]:
    """Return authenticated user context, with a demo fallback for existing MVP flows."""
    if authorization:
        scheme, _, token = authorization.partition(" ")
        if scheme.lower() == "bearer" and token:
            return await get_current_user_from_token(db, token)

    return {"user_id": "KH001", "account_id": "TK_KH001", "role": "registered", "current_plan": "free"}
