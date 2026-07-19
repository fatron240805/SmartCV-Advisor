"""Routes for premium user features."""

# Định nghĩa route cho các chức năng chỉ dành cho Premium User.

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/service-plans", tags=["Plans"])

@router.get("", summary="UC-026: Xem gói dịch vụ")
async def get_service_plans():
    # BR4: Giá dịch vụ được lấy từ hệ thống quản trị
    return {
        "data": [
            {
                "plan_id": "DV_FREE", 
                "name": "Free", 
                "price": 0, 
                "features": ["3 lượt phân tích/tháng", "Xem điểm tổng quan", "Xem lỗi phổ biến", "Lưu 3 lịch sử CV"]
            },
            {
                "plan_id": "DV_PREMIUM_30", 
                "name": "Premium - 30 Ngày", 
                "price": 99000, 
                "features": ["Phân tích CV nâng cao", "Gợi ý chi tiết & Câu mẫu chuẩn ATS", "Sao chép nhanh (1-click)", "Lịch sử không giới hạn"]
            }
        ]
    }
