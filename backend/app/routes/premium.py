"""Routes for premium user features and service plans."""

from __future__ import annotations

from typing import Any

# pyrefly: ignore [missing-import]
from fastapi import APIRouter

from app.db import db

router = APIRouter(prefix="/api/v1/service-plans", tags=["Plans"])

FREE_ROADMAP_NOTE = "Gợi ý cải thiện tổng quan, không kèm roadmap"
PREMIUM_ROADMAP_FEATURE = "Roadmap sau khi đánh giá CV"


def normalize_plan_features(plan_id: str, features: list[str]) -> list[str]:
    cleaned: list[str] = []
    for feature in features:
        normalized = feature.strip()
        if not normalized:
            continue
        lower_feature = normalized.lower()
        if plan_id == "DV_FREE" and "gợi ý cải thiện tổng quan" in lower_feature:
            if "lỗi phổ biến" in lower_feature and "Danh sách lỗi phổ biến" not in cleaned:
                cleaned.append("Danh sách lỗi phổ biến")
            continue
        cleaned.append(normalized)

    if plan_id == "DV_FREE" and FREE_ROADMAP_NOTE not in cleaned:
        cleaned.append(FREE_ROADMAP_NOTE)
    if plan_id.startswith("DV_PREMIUM") and PREMIUM_ROADMAP_FEATURE not in cleaned:
        insert_at = 2 if len(cleaned) >= 2 else len(cleaned)
        cleaned.insert(insert_at, PREMIUM_ROADMAP_FEATURE)
    return cleaned


PLANS = [
    {
        "plan_id": "DV_FREE",
        "name": "Free",
        "price": 0,
        "duration_days": None,
        "analysis_limit": 3,
        "features": [
            "3 lượt phân tích",
            "Điểm tổng quan và 5 tiêu chí",
            "Danh sách lỗi phổ biến",
            FREE_ROADMAP_NOTE,
            "Lịch sử phân tích",
        ],
        "coming_soon": [],
    },
    {
        "plan_id": "DV_PREMIUM_30",
        "name": "Premium — Job Search Pass",
        "price": 199000,
        "duration_days": 30,
        "analysis_limit": 20,
        "features": [
            "Không giới hạn lượt phân tích",
            "Gợi ý chi tiết chuyên sâu",
            PREMIUM_ROADMAP_FEATURE,
            "Câu mẫu viết lại theo STAR",
            "Sao chép nhanh từng câu mẫu",
            "Tất cả quyền lợi Free",
        ],
        "coming_soon": [
            "Matching Score với JD",
            "AI Assistant (30 lượt)",
            "Tải xuống CV đã chỉnh sửa",
        ],
    },
    {
        "plan_id": "DV_PREMIUM_90",
        "name": "Premium — Job Search Pass",
        "price": 389000,
        "duration_days": 90,
        "analysis_limit": 30,
        "features": [
            "Không giới hạn lượt phân tích",
            "Gợi ý chi tiết chuyên sâu",
            PREMIUM_ROADMAP_FEATURE,
            "Câu mẫu viết lại theo STAR",
            "Sao chép nhanh từng câu mẫu",
            "Tất cả quyền lợi Free",
        ],
        "coming_soon": [
            "Matching Score với JD",
            "AI Assistant (30 lượt)",
            "Tải xuống CV đã chỉnh sửa",
        ],
    },
]


@router.get("", summary="UC-026: Xem gói dịch vụ")
async def get_service_plans() -> dict[str, Any]:
    """Trả về danh sách gói dịch vụ từ GOIDV collection, fallback sang hardcoded nếu DB chưa có."""
    try:
        db_plans = await db["GOIDV"].find({}).to_list(length=20)
    except Exception:
        db_plans = []

    if db_plans:
        result = []
        for plan in db_plans:
            plan_id = plan.get("_id", "")
            price_raw = plan.get("Gia", 0)
            try:
                price = float(str(price_raw))
            except Exception:
                price = 0.0
            result.append(
                {
                    "plan_id": plan_id,
                    "name": plan.get("TenGoi", ""),
                    "price": int(price),
                    "duration_days": plan.get("HanSuDung"),
                    "analysis_limit": plan.get("SoLuotPhanTich"),
                    "features": normalize_plan_features(
                        plan_id,
                        [f.strip() for f in (plan.get("QuyenLoi") or "").split(";") if f.strip()],
                    ),
                    "coming_soon": [],
                }
            )
        return {"data": result}

    # Fallback: trả về danh sách hardcoded đầy đủ cả 30 và 90 ngày
    return {
        "data": [
            {
                "plan_id": "DV_FREE",
                "name": "Free",
                "price": 0,
                "duration_days": None,
                "analysis_limit": 3,
                "features": [
                    "3 lượt phân tích",
                    "Điểm tổng quan và 5 tiêu chí",
                    "Danh sách lỗi phổ biến",
                    FREE_ROADMAP_NOTE,
                    "Lịch sử phân tích",
                ],
                "coming_soon": [],
            },
            {
                "plan_id": "DV_PREMIUM_30",
                "name": "Premium — Job Search Pass",
                "price": 199000,
                "duration_days": 30,
                "analysis_limit": 20,
                "features": [
                    "Không giới hạn lượt phân tích",
                    "Gợi ý chi tiết chuyên sâu",
                    PREMIUM_ROADMAP_FEATURE,
                    "Câu mẫu viết lại theo STAR",
                    "Sao chép nhanh từng câu mẫu",
                    "Tất cả quyền lợi Free",
                ],
                "coming_soon": [
                    "Matching Score với JD",
                    "AI Assistant (30 lượt)",
                    "Tải xuống CV đã chỉnh sửa",
                ],
            },
            {
                "plan_id": "DV_PREMIUM_90",
                "name": "Premium — Job Search Pass",
                "price": 389000,
                "duration_days": 90,
                "analysis_limit": 30,
                "features": [
                    "Không giới hạn lượt phân tích",
                    "Gợi ý chi tiết chuyên sâu",
                    PREMIUM_ROADMAP_FEATURE,
                    "Câu mẫu viết lại theo STAR",
                    "Sao chép nhanh từng câu mẫu",
                    "Tất cả quyền lợi Free",
                ],
                "coming_soon": [
                    "Matching Score với JD",
                    "AI Assistant (30 lượt)",
                    "Tải xuống CV đã chỉnh sửa",
                ],
            },
        ]
    }
