from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from bson.decimal128 import Decimal128
from pymongo import ASCENDING, DESCENDING, IndexModel, UpdateOne
from pymongo.errors import CollectionInvalid, OperationFailure


# Các collection/index nền tảng của nhóm use case MVP ở bước 4.
# Hàm bootstrap bên dưới tuyệt đối không chèn dữ liệu mẫu.
MVP_COLLECTIONS = (
    "ADMIN",
    "KHACHHANG",
    "TAIKHOAN",
    "REFRESH_TOKENS",
    "NGANHNGHIET",
    "KYNANG",
    "NGANHNGHE_KYNANG",
    "DIEMDANHGIA",
    "CV",
    "KETQUA_PTCV",
    "LICHSUPTCV",
    "GOIY_CAITHIEN",
    "LOG_ADMIN",
    "LOG_KH",
    "LUOTDUNG",
    "DATA_DELETION_REQUESTS",
    "SCORING_CONFIG_VERSIONS",
    "DANHGIASP",
    "SUKIEN_SANPHAM",
    "GOIDV",
)

DEFAULT_PREMIUM_COMING_SOON = (
    "Danh sách lỗi chi tiết; Câu mẫu viết lại theo STAR; "
    "Sao chép nhanh từng câu mẫu; Nội dung viết lại nâng cao; "
    "Matching Score với mô tả công việc; AI Assistant hỗ trợ chỉnh sửa CV; "
    "Tải xuống CV đã chỉnh sửa"
)

LEGACY_FEEDBACK_UNIQUE_INDEX_NAME = "uq_danhgiasp_makh_machuky"
FEEDBACK_LIFECYCLE_INDEX_NAME = "idx_danhgiasp_makh_machuky_ngaytao"

DEFAULT_SERVICE_PLANS: tuple[dict[str, Any], ...] = (
    {
        "_id": "DV_FREE",
        "TenGoi": "Free",
        "Gia": Decimal128("0.00"),
        "HanSuDung": -1,
        "SoLuotPhanTich": 3,
        "QuyenLoi": "3 lượt phân tích trong chu kỳ; xem điểm và gợi ý cơ bản; xem toàn bộ lịch sử phân tích",
        "SapRaMat": "",
        "TrangThai": "active",
    },
    {
        "_id": "DV_PREMIUM_30",
        "TenGoi": "Premium - Job Search Pass 30 ngày",
        "Gia": Decimal128("199000.00"),
        "HanSuDung": 30,
        "SoLuotPhanTich": -1,
        "QuyenLoi": "Phân tích không giới hạn; roadmap cải thiện; gợi ý chuyên sâu; xem toàn bộ lịch sử phân tích",
        "SapRaMat": DEFAULT_PREMIUM_COMING_SOON,
        "TrangThai": "active",
    },
    {
        "_id": "DV_PREMIUM_90",
        "TenGoi": "Premium - Job Search Pass 90 ngày",
        "Gia": Decimal128("389000.00"),
        "HanSuDung": 90,
        "SoLuotPhanTich": -1,
        "QuyenLoi": "Phân tích không giới hạn; roadmap cải thiện; gợi ý chuyên sâu; xem toàn bộ lịch sử phân tích",
        "SapRaMat": DEFAULT_PREMIUM_COMING_SOON,
        "TrangThai": "active",
    },
)

MVP_INDEXES: dict[str, list[tuple[list[tuple[str, int]], dict[str, Any]]]] = {
    "ADMIN": [
        ([("Email", ASCENDING)], {"name": "uq_admin_email", "unique": True}),
    ],
    "KHACHHANG": [
        ([("Email", ASCENDING)], {"name": "uq_khachhang_email", "unique": True}),
    ],
    "TAIKHOAN": [
        ([("Email", ASCENDING)], {"name": "uq_taikhoan_email", "unique": True}),
        ([("MaKH", ASCENDING)], {"name": "uq_taikhoan_makh", "unique": True, "sparse": True}),
        ([("MaADM", ASCENDING)], {"name": "uq_taikhoan_maadm", "unique": True, "sparse": True}),
        ([("EmailNormalized", ASCENDING)], {"name": "idx_taikhoan_email_normalized", "sparse": True}),
        (
            [("EmailVerificationTokenHash", ASCENDING)],
            {"name": "idx_taikhoan_email_verification_token", "sparse": True},
        ),
        (
            [("LastEmailVerificationTokenHash", ASCENDING)],
            {"name": "idx_taikhoan_last_email_verification_token", "sparse": True},
        ),
        (
            [("PasswordResetTokenHash", ASCENDING)],
            {"name": "idx_taikhoan_password_reset_token", "sparse": True},
        ),
        ([("CreatedAt", DESCENDING)], {"name": "idx_taikhoan_created_at"}),
    ],
    "REFRESH_TOKENS": [
        ([("TokenHash", ASCENDING)], {"name": "uq_refresh_token_hash", "unique": True}),
        (
            [("MaTK", ASCENDING), ("RevokedAt", ASCENDING)],
            {"name": "idx_refresh_token_account_revoked"},
        ),
        (
            [("ExpiresAt", ASCENDING)],
            {"name": "ttl_refresh_token_expiry", "expireAfterSeconds": 0},
        ),
    ],
    "NGANHNGHIET": [
        (
            [("TenNganhNormalized", ASCENDING)],
            {"name": "uq_nganh_ten_normalized", "unique": True, "sparse": True},
        ),
        ([("TenNganh", ASCENDING)], {"name": "idx_nganh_ten"}),
    ],
    "KYNANG": [
        (
            [("TenKyNangNormalized", ASCENDING)],
            {"name": "uq_kynang_ten_normalized", "unique": True, "sparse": True},
        ),
    ],
    "NGANHNGHE_KYNANG": [
        (
            [("MaNganh", ASCENDING), ("MaKyNang", ASCENDING)],
            {"name": "uq_nganhnghe_kynang", "unique": True},
        ),
    ],
    "DIEMDANHGIA": [
        (
            [("MaNganh", ASCENDING), ("MaKyNang", ASCENDING)],
            {"name": "uq_diemdanhgia_manganh_makynang", "unique": True, "sparse": True},
        ),
        ([("MaKyNang", ASCENDING)], {"name": "idx_diemdanhgia_makynang"}),
    ],
    "CV": [
        ([("MaKH", ASCENDING)], {"name": "idx_cv_makh"}),
        ([("MaNganh", ASCENDING)], {"name": "idx_cv_manganh"}),
        (
            [("MaKH", ASCENDING), ("NgayTaiLen", DESCENDING)],
            {"name": "idx_cv_makh_ngaytailen"},
        ),
    ],
    "KETQUA_PTCV": [
        ([("MaCV", ASCENDING)], {"name": "idx_ketqua_macv"}),
        ([("MaNganh", ASCENDING)], {"name": "idx_ketqua_manganh"}),
    ],
    "LICHSUPTCV": [
        (
            [("MaKH", ASCENDING), ("NgayPT", DESCENDING)],
            {"name": "idx_lichsu_khachhang_ngay"},
        ),
        ([("MaKQ", ASCENDING)], {"name": "idx_lichsu_makq"}),
    ],
    "GOIY_CAITHIEN": [
        (
            [("MaKQ", ASCENDING), ("DoUuTien", ASCENDING)],
            {"name": "idx_goiy_ketqua_uutien"},
        ),
    ],
    "LOG_ADMIN": [
        (
            [("MaADM", ASCENDING), ("ThoiDiemThucHien", ASCENDING)],
            {"name": "idx_logadmin_admin_time"},
        ),
    ],
    "LOG_KH": [
        (
            [("MaKH", ASCENDING), ("ThoiDiemThucHien", ASCENDING)],
            {"name": "idx_logkh_khachhang_time"},
        ),
        (
            [("MaKH", ASCENDING), ("DoiTuong", ASCENDING), ("MaDoiTuong", ASCENDING)],
            {"name": "idx_logkh_owner_target"},
        ),
    ],
    "LUOTDUNG": [
        (
            [("MaKH", ASCENDING), ("MaGoiDV", ASCENDING), ("NgayBatDau", DESCENDING)],
            {"name": "idx_luotdung_customer_plan_start"},
        ),
        (
            [("MaKH", ASCENDING), ("MaGoiDV", ASCENDING), ("HanSuDung", DESCENDING)],
            {"name": "idx_luotdung_customer_plan_expiry"},
        ),
    ],
    "DATA_DELETION_REQUESTS": [
        (
            [("MaKH", ASCENDING), ("RequestedAt", DESCENDING)],
            {"name": "idx_data_deletion_customer_requested"},
        ),
        (
            [("MaKH", ASCENDING), ("Scope", ASCENDING), ("Status", ASCENDING)],
            {"name": "idx_data_deletion_customer_scope_status"},
        ),
    ],
    "SCORING_CONFIG_VERSIONS": [
        (
            [("MaNganh", ASCENDING), ("CreatedAt", ASCENDING)],
            {"name": "idx_scoring_config_role_time"},
        ),
    ],
    "DANHGIASP": [
        (
            [("MaKH", ASCENDING), ("MaChuKy", ASCENDING), ("NgayTao", DESCENDING)],
            {
                "name": FEEDBACK_LIFECYCLE_INDEX_NAME,
            },
        ),
        (
            [
                ("LoaiPhanHoi", ASCENDING),
                ("TrangThai", ASCENDING),
                ("NgayTao", DESCENDING),
            ],
            {
                "name": "idx_danhgiasp_loai_trangthai_ngaytao",
            },
        ),
        (
            [("TrangThai", ASCENDING), ("NgayTao", DESCENDING)],
            {
                "name": "idx_danhgiasp_trangthai_ngaytao",
            },
        ),
        (
            [("DanhGia", ASCENDING), ("NgayTao", DESCENDING)],
            {
                "name": "idx_danhgiasp_danhgia_ngaytao",
            },
        ),
        (
            [("MaKQ", ASCENDING)],
            {
                "name": "idx_danhgiasp_makq",
            },
        ),
        (
            [("NgayTao", DESCENDING)],
            {
                "name": "idx_danhgiasp_ngaytao",
            },
        ),
    ],
    "SUKIEN_SANPHAM": [
        (
            [("LoaiSuKien", ASCENDING), ("ThoiDiem", DESCENDING)],
            {
                "name": "idx_sukien_ten_thoidiem",
            },
        ),
        (
            [("MaKH", ASCENDING), ("ThoiDiem", DESCENDING)],
            {
                "name": "idx_sukien_makh_thoidiem",
            },
        ),
        (
            [("SessionId", ASCENDING), ("ThoiDiem", DESCENDING)],
            {
                "name": "idx_sukien_maphien_thoidiem",
            },
        ),
        (
            [("LoaiSuKien", ASCENDING), ("ActorKey", ASCENDING), ("ThoiDiem", DESCENDING)],
            {
                "name": "idx_sukien_actor_loai",
            },
        ),
        (
            [("DedupeKey", ASCENDING)],
            {
                "name": "uq_sukien_dedupe_key",
                "unique": True,
                "sparse": True,
            },
        ),
        (
            [("LoaiSuKien", ASCENDING), ("NguonTruyCap", ASCENDING), ("ThoiDiem", DESCENDING)],
            {"name": "idx_sukien_loai_nguon_thoidiem"},
        ),
        (
            [("LoaiSuKien", ASCENDING), ("Campaign", ASCENDING), ("ThoiDiem", DESCENDING)],
            {"name": "idx_sukien_loai_campaign_thoidiem"},
        ),
        (
            [("LoaiSuKien", ASCENDING), ("MessageVariant", ASCENDING), ("ThoiDiem", DESCENDING)],
            {"name": "idx_sukien_loai_variant_thoidiem"},
        ),
        (
            [
                ("NguonTruyCap", ASCENDING),
                ("Campaign", ASCENDING),
                ("MessageVariant", ASCENDING),
                ("ThoiDiem", DESCENDING),
            ],
            {
                "name": "idx_sukien_attribution_thoidiem",
            },
        ),
        (
            [("MaNganh", ASCENDING), ("ThoiDiem", DESCENDING)],
            {
                "name": "idx_sukien_manganh_thoidiem",
            },
        ),
        (
            [("MaKH", ASCENDING), ("MaCV", ASCENDING)],
            {"name": "idx_sukien_makh_macv"},
        ),
        (
            [("MaKH", ASCENDING), ("MaKQ", ASCENDING)],
            {"name": "idx_sukien_makh_makq"},
        ),
    ],
    "GOIDV": [
        (
            [("TrangThai", ASCENDING)],
            {
                "name": "idx_goidv_trangthai",
            },
        ),
        (
            [("TrangThai", ASCENDING), ("Gia", ASCENDING)],
            {"name": "idx_goidv_trangthai_gia"},
        ),
        (
            [("NgayCapNhat", DESCENDING)],
            {"name": "idx_goidv_ngaycapnhat"},
        ),
    ],
}


_BOOTSTRAPPED_DATABASES: set[int] = set()


async def drop_legacy_feedback_unique_index(collection: Any) -> None:
    """Remove the former one-feedback-per-lifecycle constraint safely.

    The migration only drops an index; existing feedback documents are never
    changed or deleted. Detecting the key pattern also covers installations
    where the legacy index was created under a different name.
    """

    indexes = await collection.list_indexes().to_list(length=None)
    for index in indexes:
        key = index.get("key") or {}
        key_items = list(key.items()) if hasattr(key, "items") else []
        is_legacy_name = index.get("name") == LEGACY_FEEDBACK_UNIQUE_INDEX_NAME
        is_legacy_unique_pattern = bool(index.get("unique")) and key_items == [
            ("MaKH", ASCENDING),
            ("MaChuKy", ASCENDING),
        ]
        if not (is_legacy_name or is_legacy_unique_pattern):
            continue

        try:
            await collection.drop_index(index["name"])
        except OperationFailure as exc:
            # Another application instance may have completed the same
            # idempotent migration after list_indexes() returned.
            if getattr(exc, "code", None) != 27 and "index not found" not in str(exc).lower():
                raise


async def drop_legacy_score_unique_index(collection: Any) -> None:
    """Remove the legacy global-per-skill constraint before role scoring."""

    indexes = await collection.list_indexes().to_list(length=None)
    for index in indexes:
        key = index.get("key") or {}
        key_items = list(key.items()) if hasattr(key, "items") else []
        is_legacy = index.get("name") == "uq_diemdanhgia_makynang" or (
            bool(index.get("unique")) and key_items == [("MaKyNang", ASCENDING)]
        )
        if not is_legacy:
            continue
        try:
            await collection.drop_index(index["name"])
        except OperationFailure as exc:
            if getattr(exc, "code", None) != 27 and "index not found" not in str(exc).lower():
                raise


async def ensure_mvp_collections(db: Any) -> None:
    """Tạo idempotent các collection và index cần cho MVP bước 4."""

    database_key = id(db)
    if database_key in _BOOTSTRAPPED_DATABASES:
        return

    existing_collections = set(await db.list_collection_names())

    for collection_name in MVP_COLLECTIONS:
        if collection_name not in existing_collections:
            try:
                await db.create_collection(collection_name)
            except CollectionInvalid:
                # Một process khởi động song song có thể vừa tạo collection.
                pass

    # This must run before creating the replacement non-unique index. It is
    # intentionally repeated on every bootstrap so deployments that upgrade
    # after a temporary database outage migrate on the next successful call.
    await drop_legacy_feedback_unique_index(db["DANHGIASP"])
    await drop_legacy_score_unique_index(db["DIEMDANHGIA"])

    for collection_name, index_definitions in MVP_INDEXES.items():
        collection = db[collection_name]
        # One command per collection avoids a network round-trip per index on
        # remote MongoDB deployments such as Atlas.
        await collection.create_indexes(
            [IndexModel(keys, **options) for keys, options in index_definitions]
        )

    _BOOTSTRAPPED_DATABASES.add(database_key)


async def ensure_default_service_plans(db: Any) -> None:
    """Install defaults and enforce canonical plan-duration invariants."""
    now = datetime.now(timezone.utc)
    operations: list[UpdateOne] = []
    for plan in DEFAULT_SERVICE_PLANS:
        plan_id = plan["_id"]
        operations.append(
            UpdateOne(
                {"_id": plan_id},
                {
                    "$setOnInsert": {
                        **{key: value for key, value in plan.items() if key != "_id"},
                        "NgayTao": now,
                        "NgayCapNhat": now,
                        "MaADM": "SYSTEM",
                    }
                },
                upsert=True,
            )
        )
        # Duration is part of the plan identity, not an Admin-customizable
        # benefit. This also migrates legacy DV_FREE values such as 30/365 to -1.
        operations.append(
            UpdateOne(
                {"_id": plan_id, "HanSuDung": {"$ne": plan["HanSuDung"]}},
                {"$set": {"HanSuDung": plan["HanSuDung"]}},
            )
        )
        # Migrate legacy documents once without resetting later Admin edits.
        operations.append(
            UpdateOne(
                {"_id": plan_id, "SapRaMat": {"$exists": False}},
                {"$set": {"SapRaMat": plan["SapRaMat"]}},
            )
        )

    if operations:
        await db["GOIDV"].bulk_write(operations, ordered=True)
