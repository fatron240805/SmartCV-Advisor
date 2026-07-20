"""Shared FastAPI dependencies for request context."""


async def get_current_user() -> dict[str, str]:
    """Temporary auth dependency until UC-008..UC-011 are fully wired."""
    return {"user_id": "KH001", "current_plan": "free"}
