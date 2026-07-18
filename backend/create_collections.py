import os
import asyncio
from datetime import datetime, timedelta, timezone

from bson.decimal128 import Decimal128
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING


load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB = os.getenv("MONGODB_DB", "smartcv")


async def main():
    if not MONGODB_URI:
        raise RuntimeError(
            "Chưa cấu hình MONGODB_URI trong file .env"
        )

    client = AsyncIOMotorClient(
        MONGODB_URI,
        serverSelectionTimeoutMS=5000,
    )

    try:
        # Kiểm tra kết nối MongoDB
        await client.admin.command("ping")
        print("Connected to MongoDB successfully.")

        db = client[MONGODB_DB]

        now = datetime.now(timezone.utc)

        # =============================================================
        # DANH SÁCH COLLECTION VÀ DỮ LIỆU MẪU
        # =============================================================

        collections = [
            # ---------------------------------------------------------
            # 1. ADMIN
            # ---------------------------------------------------------
            {
                "name": "ADMIN",
                "documents": [
                    {
                        "_id": "ADM001",
                        "HoTen": "Quản trị viên SmartCV",
                        "Email": "admin@smartcv.vn",
                        "SoDienThoai": "0900000001",
                        "DiaChi": "TP. Hồ Chí Minh",
                        "TrangThai": "Hoat dong",
                    }
                ],
            },

            # ---------------------------------------------------------
            # 2. KHACHHANG
            # ---------------------------------------------------------
            {
                "name": "KHACHHANG",
                "documents": [
                    {
                        "_id": "KH001",
                        "HoTen": "Trần Minh An",
                        "Email": "minhan@example.com",
                        "SoDienThoai": "0901234567",
                        "DiaChi": "TP. Hồ Chí Minh",
                        "TrangThai": "Hoạt động",
                        "LoaiKH": "registered",
                        "TrinhDoHV": "Sinh viên năm cuối",
                        "ViTriNN": "Frontend Developer",
                        "NNQuanTam": "Công nghệ thông tin",
                        "NgayDangKy": now,
                    },
                    {
                        "_id": "KH002",
                        "HoTen": "Nguyễn Hoàng Nam",
                        "Email": "hoangnam@example.com",
                        "SoDienThoai": "0912345678",
                        "DiaChi": "Bình Dương",
                        "TrangThai": "Hoạt động",
                        "LoaiKH": "premium",
                        "TrinhDoHV": "Đã tốt nghiệp",
                        "ViTriNN": "Backend Developer",
                        "NNQuanTam": "Phát triển phần mềm",
                        "NgayDangKy": now,
                    },
                ],
            },

            # ---------------------------------------------------------
            # 3. TAIKHOAN
            # ---------------------------------------------------------
            {
                "name": "TAIKHOAN",
                "documents": [
                    {
                        "_id": "TK_ADM001",
                        "Email": "admin@smartcv.vn",

                        # Thay bằng password hash bcrypt thật
                        "Matkhau": "CHANGE_ME_BCRYPT_HASH",

                        "MaADM": "ADM001",
                    },
                    {
                        "_id": "TK_KH001",
                        "Email": "minhan@example.com",
                        "Matkhau": "CHANGE_ME_BCRYPT_HASH",
                        "MaKH": "KH001",
                    },
                    {
                        "_id": "TK_KH002",
                        "Email": "hoangnam@example.com",
                        "Matkhau": "CHANGE_ME_BCRYPT_HASH",
                        "MaKH": "KH002",
                    },
                ],
            },

            # ---------------------------------------------------------
            # 4. GOIDV
            # ---------------------------------------------------------
            {
                "name": "GOIDV",
                "documents": [
                    {
                        "_id": "DV_FREE",
                        "TenGoi": "Free",
                        "Gia": Decimal128("0.00"),
                        "SoLuotPhanTich": 3,
                        "HanSuDung": 30,
                        "QuyenLoi": (
                            "3 lượt phân tích mỗi tháng; xem điểm tổng quan; "
                            "xem lỗi phổ biến và gợi ý cải thiện tổng quan."
                        ),
                        "NgayTao": now,
                        "NgayCapNhat": None,
                        "MaADM": "ADM001",
                    },
                    {
                        "_id": "DV_PREMIUM_30",
                        "TenGoi": "Premium - Job Search Pass 30 ngày",
                        "Gia": Decimal128("99000.00"),
                        "SoLuotPhanTich": 20,
                        "HanSuDung": 30,
                        "QuyenLoi": (
                            "Phân tích CV nâng cao; xem gợi ý chi tiết; "
                            "xem câu mẫu viết lại và sao chép nhanh."
                        ),
                        "NgayTao": now,
                        "NgayCapNhat": None,
                        "MaADM": "ADM001",
                    },
                    {
                        "_id": "DV_PREMIUM_90",
                        "TenGoi": "Premium - Job Search Pass 90 ngày",
                        "Gia": Decimal128("297000.00"),
                        "SoLuotPhanTich": 30,
                        "HanSuDung": 90,
                        "QuyenLoi": (
                            "Phân tích CV nâng cao; xem gợi ý chi tiết; "
                            "xem câu mẫu viết lại và sao chép nhanh."
                        ),
                        "NgayTao": now,
                        "NgayCapNhat": None,
                        "MaADM": "ADM001",
                    },
                ],
            },

            # ---------------------------------------------------------
            # 5. LOG_ADMIN
            # ---------------------------------------------------------
            {
                "name": "LOG_ADMIN",
                "documents": [
                    {
                        "_id": "LOG_ADM001",
                        "HanhDong": "Tạo gói dịch vụ",
                        "DuLieuTruoc": None,
                        "DuLieuSau": {
                            "MaDV": "DV_PREMIUM_30",
                            "TenGoi": "Premium - Job Search Pass 30 ngày",
                        },
                        "KetQua": "Thanh cong",
                        "ThoiDiemThucHien": now,
                        "MaADM": "ADM001",
                        "DoiTuong": "GOIDV",
                        "MaDoiTuong": "DV_PREMIUM_30",
                    },
                    {
                        "_id": "LOG_ADM001",
                        "HanhDong": "Tạo gói dịch vụ",
                        "DuLieuTruoc": None,
                        "DuLieuSau": {
                            "MaDV": "DV_PREMIUM_90",
                            "TenGoi": "Premium - Job Search Pass 90 ngày",
                        },
                        "KetQua": "Thanh cong",
                        "ThoiDiemThucHien": now,
                        "MaADM": "ADM001",
                        "DoiTuong": "GOIDV",
                        "MaDoiTuong": "DV_PREMIUM_90",
                    },
                ],
            },

            # ---------------------------------------------------------
            # 6. LOG_KH
            # ---------------------------------------------------------
            {
                "name": "LOG_KH",
                "documents": [
                    {
                        "_id": "LOG_KH001",
                        "HanhDong": "Tải CV lên hệ thống",
                        "DuLieuTruoc": None,
                        "DuLieuSau": {
                            "TenFileGoc": "Tran_Minh_An_Frontend_CV.pdf",
                            "TrangThai": "uploaded",
                        },
                        "KetQua": "Thanh cong",
                        "ThoiDiemThucHien": now,
                        "MaKH": "KH001",
                        "DoiTuong": "CV",
                        "MaDoiTuong": "CV001",
                    }
                ],
            },

            # ---------------------------------------------------------
            # 7. LUOTDUNG
            # ---------------------------------------------------------
            {
                "name": "LUOTDUNG",
                "documents": [
                    {
                        "_id": "LD001",
                        "SoLuongDaDung": 1,
                        "GioiHanTheoDoi": 3,
                        "ThoiDiemSuDung": now,
                        "HanSuDung": now + timedelta(days=30),
                        "QuyenLoi": (
                            "Phân tích CV cơ bản và xem gợi ý tổng quan."
                        ),
                        "MaKH": "KH001",
                    },
                    {
                        "_id": "LD002",
                        "SoLuongDaDung": 4,
                        "GioiHanTheoDoi": 30,
                        "ThoiDiemSuDung": now,
                        "HanSuDung": now + timedelta(days=30),
                        "QuyenLoi": (
                            "Xem gợi ý chi tiết và câu mẫu Premium."
                        ),
                        "MaKH": "KH002",
                    },
                ],
            },

            # ---------------------------------------------------------
            # 8. NGANHNGHIET
            # Giữ nguyên tên bảng theo ERD hiện tại
            # ---------------------------------------------------------
            {
                "name": "NGANHNGHIET",
                "documents": [
                    {
                        "_id": "NG_FRONTEND",
                        "TenNganh": "Frontend Developer",
                        "MoTa": (
                            "Phát triển giao diện web với HTML, CSS, "
                            "JavaScript và các thư viện frontend."
                        ),
                        "NgayTao": now,
                        "NgayCapNhat": None,
                        "TrangThai": "hoat dong",
                    },
                    {
                        "_id": "NG_BACKEND",
                        "TenNganh": "Backend Developer",
                        "MoTa": (
                            "Phát triển API, xử lý nghiệp vụ, cơ sở dữ liệu "
                            "và các dịch vụ phía máy chủ."
                        ),
                        "NgayTao": now,
                        "NgayCapNhat": None,
                        "TrangThai": "hoat dong",
                    },
                ],
            },

            # ---------------------------------------------------------
            # 9. KYNANG
            # ---------------------------------------------------------
            {
                "name": "KYNANG",
                "documents": [
                    {
                        "_id": "KN_REACT",
                        "TenKyNang": "ReactJS",
                        "MoTa": "Thư viện xây dựng giao diện web.",
                        "NgayTao": now,
                        "NgayCapNhat": None,
                        "TrangThai": "hoat dong",
                    },
                    {
                        "_id": "KN_REST_API",
                        "TenKyNang": "REST API",
                        "MoTa": "Thiết kế và sử dụng API theo kiến trúc REST.",
                        "NgayTao": now,
                        "NgayCapNhat": None,
                        "TrangThai": "hoat dong",
                    },
                    {
                        "_id": "KN_GIT",
                        "TenKyNang": "Git",
                        "MoTa": "Quản lý phiên bản mã nguồn.",
                        "NgayTao": now,
                        "NgayCapNhat": None,
                        "TrangThai": "hoat dong",
                    },
                    {
                        "_id": "KN_PYTHON",
                        "TenKyNang": "Python",
                        "MoTa": "Ngôn ngữ lập trình Python.",
                        "NgayTao": now,
                        "NgayCapNhat": None,
                        "TrangThai": "hoat dong",
                    },
                    {
                        "_id": "KN_MONGODB",
                        "TenKyNang": "MongoDB",
                        "MoTa": "Cơ sở dữ liệu NoSQL dạng document.",
                        "NgayTao": now,
                        "NgayCapNhat": None,
                        "TrangThai": "hoat dong",
                    },
                ],
            },

            # ---------------------------------------------------------
            # 10. NGANHNGHE_KYNANG
            # ---------------------------------------------------------
            {
                "name": "NGANHNGHE_KYNANG",
                "documents": [
                    {
                        "_id": "NNKN_FRONTEND_REACT",
                        "MaNganh": "NG_FRONTEND",
                        "MaKyNang": "KN_REACT",
                    },
                    {
                        "_id": "NNKN_FRONTEND_REST",
                        "MaNganh": "NG_FRONTEND",
                        "MaKyNang": "KN_REST_API",
                    },
                    {
                        "_id": "NNKN_FRONTEND_GIT",
                        "MaNganh": "NG_FRONTEND",
                        "MaKyNang": "KN_GIT",
                    },
                    {
                        "_id": "NNKN_BACKEND_PYTHON",
                        "MaNganh": "NG_BACKEND",
                        "MaKyNang": "KN_PYTHON",
                    },
                    {
                        "_id": "NNKN_BACKEND_MONGODB",
                        "MaNganh": "NG_BACKEND",
                        "MaKyNang": "KN_MONGODB",
                    },
                    {
                        "_id": "NNKN_BACKEND_REST",
                        "MaNganh": "NG_BACKEND",
                        "MaKyNang": "KN_REST_API",
                    },
                ],
            },

            # ---------------------------------------------------------
            # 11. DIEMDANHGIA
            # ---------------------------------------------------------
            {
                "name": "DIEMDANHGIA",
                "documents": [
                    {
                        "_id": "DDG_REACT",
                        "MaKyNang": "KN_REACT",
                        "Diem": 3.0,
                        "TrongSo": 25.0,
                        "MucDo": "Core Skill",
                        "NgayCapNhat": now,
                    },
                    {
                        "_id": "DDG_REST_API",
                        "MaKyNang": "KN_REST_API",
                        "Diem": 2.0,
                        "TrongSo": 15.0,
                        "MucDo": "Important",
                        "NgayCapNhat": now,
                    },
                    {
                        "_id": "DDG_GIT",
                        "MaKyNang": "KN_GIT",
                        "Diem": 2.0,
                        "TrongSo": 10.0,
                        "MucDo": "Important",
                        "NgayCapNhat": now,
                    },
                    {
                        "_id": "DDG_PYTHON",
                        "MaKyNang": "KN_PYTHON",
                        "Diem": 3.0,
                        "TrongSo": 25.0,
                        "MucDo": "Core Skill",
                        "NgayCapNhat": now,
                    },
                    {
                        "_id": "DDG_MONGODB",
                        "MaKyNang": "KN_MONGODB",
                        "Diem": 2.0,
                        "TrongSo": 15.0,
                        "MucDo": "Important",
                        "NgayCapNhat": now,
                    },
                ],
            },

            # ---------------------------------------------------------
            # 12. CV
            # ---------------------------------------------------------
            {
                "name": "CV",
                "documents": [
                    {
                        "_id": "CV001",
                        "Loai": "pdf",
                        "DungLuong": 1843,
                        "TenFileGoc": "Tran_Minh_An_Frontend_CV.pdf",
                        "NgayTaiLen": now,
                        "TrangThai": "completed",
                        "MaNganh": "NG_FRONTEND",
                        "MaKH": "KH001",
                    },
                    {
                        "_id": "CV002",
                        "Loai": "docx",
                        "DungLuong": 956,
                        "TenFileGoc": "Nguyen_Hoang_Nam_Backend_CV.docx",
                        "NgayTaiLen": now,
                        "TrangThai": "uploaded",
                        "MaNganh": "NG_BACKEND",
                        "MaKH": "KH002",
                    },
                ],
            },

            # ---------------------------------------------------------
            # 13. KETQUA_PTCV
            # ---------------------------------------------------------
            {
                "name": "KETQUA_PTCV",
                "documents": [
                    {
                        "_id": "KQ001",
                        "DiemTongQuan": 72.0,

                        # Professional Summary
                        "DiemPhanGT": 7.0,

                        # Education
                        "DiemTDHV": 8.0,

                        # Experience
                        "DiemKNLV": 12.0,

                        # Projects
                        "DiemDoAn": 10.0,

                        # Technical Skills
                        "DiemTechSkill": 27.0,

                        # Certifications
                        "DiemCert": 8.0,

                        "NhanXetTQ": (
                            "CV có cấu trúc rõ ràng nhưng cần bổ sung kết quả "
                            "định lượng, thống nhất mốc thời gian và làm rõ "
                            "các kỹ năng đã sử dụng trong dự án."
                        ),
                        "ThoiDiemPT": now,
                        "MaCV": "CV001",
                    }
                ],
            },

            # ---------------------------------------------------------
            # 14. LICHSUPTCV
            # ---------------------------------------------------------
            {
                "name": "LICHSUPTCV",
                "documents": [
                    {
                        "_id": "LS001",
                        "NgayPT": now,
                        "MaKQ": "KQ001",
                        "MaKH": "KH001",
                    }
                ],
            },

            # ---------------------------------------------------------
            # 15. GOIY_CAITHIEN
            # ---------------------------------------------------------
            {
                "name": "GOIY_CAITHIEN",
                "documents": [
                    {
                        "_id": "GY001",
                        "MoTaVanDe": (
                            "Mô tả dự án chưa thể hiện kết quả định lượng."
                        ),
                        "GiaiPhap": (
                            "Bổ sung số liệu cụ thể như số màn hình đã phát "
                            "triển, thời gian xử lý hoặc tỷ lệ cải thiện."
                        ),
                        "Loai": "noi dung",
                        "is_premium": False,
                        "DoUuTien": 1,
                        "MaKQ": "KQ001",
                    },
                    {
                        "_id": "GY002",
                        "MoTaVanDe": (
                            "CV chưa thể hiện rõ kỹ năng REST API và Git."
                        ),
                        "GiaiPhap": (
                            "Đưa các kỹ năng thực sự đã sử dụng vào phần "
                            "Kỹ năng và mô tả chúng trong dự án liên quan."
                        ),
                        "Loai": "tu khoa",
                        "is_premium": False,
                        "DoUuTien": 2,
                        "MaKQ": "KQ001",
                    },
                    {
                        "_id": "GY003",
                        "MoTaVanDe": (
                            "Câu mô tả kinh nghiệm còn chung chung."
                        ),
                        "GiaiPhap": (
                            "Viết lại câu mô tả theo hướng hành động, "
                            "nhiệm vụ và kết quả đạt được."
                        ),
                        "Loai": "noi dung",
                        "is_premium": True,
                        "DoUuTien": 3,
                        "MaKQ": "KQ001",
                    },
                ],
            },
        ]

        # =============================================================
        # INDEX TƯƠNG ĐƯƠNG UNIQUE / PRIMARY KEY / FOREIGN KEY TRA CỨU
        # =============================================================

        indexes = {
            "ADMIN": [
                (
                    [("Email", ASCENDING)],
                    {
                        "unique": True,
                        "name": "uq_admin_email",
                    },
                )
            ],
            "KHACHHANG": [
                (
                    [("Email", ASCENDING)],
                    {
                        "unique": True,
                        "name": "uq_khachhang_email",
                    },
                )
            ],
            "TAIKHOAN": [
                (
                    [("Email", ASCENDING)],
                    {
                        "unique": True,
                        "name": "uq_taikhoan_email",
                    },
                ),
                (
                    [("MaKH", ASCENDING)],
                    {
                        "unique": True,
                        "sparse": True,
                        "name": "uq_taikhoan_makh",
                    },
                ),
                (
                    [("MaADM", ASCENDING)],
                    {
                        "unique": True,
                        "sparse": True,
                        "name": "uq_taikhoan_maadm",
                    },
                ),
            ],
            "NGANHNGHE_KYNANG": [
                (
                    [
                        ("MaNganh", ASCENDING),
                        ("MaKyNang", ASCENDING),
                    ],
                    {
                        "unique": True,
                        "name": "uq_nganhnghe_kynang",
                    },
                )
            ],
            "DIEMDANHGIA": [
                (
                    [("MaKyNang", ASCENDING)],
                    {
                        "unique": True,
                        "name": "uq_diemdanhgia_makynang",
                    },
                )
            ],
            "CV": [
                (
                    [("MaKH", ASCENDING)],
                    {
                        "name": "idx_cv_makh",
                    },
                ),
                (
                    [("MaNganh", ASCENDING)],
                    {
                        "name": "idx_cv_manganh",
                    },
                ),
            ],
            "KETQUA_PTCV": [
                (
                    [("MaCV", ASCENDING)],
                    {
                        "name": "idx_ketqua_macv",
                    },
                )
            ],
            "LICHSUPTCV": [
                (
                    [
                        ("MaKH", ASCENDING),
                        ("NgayPT", ASCENDING),
                    ],
                    {
                        "name": "idx_lichsu_khachhang_ngay",
                    },
                ),
                (
                    [("MaKQ", ASCENDING)],
                    {
                        "name": "idx_lichsu_makq",
                    },
                ),
            ],
            "GOIY_CAITHIEN": [
                (
                    [
                        ("MaKQ", ASCENDING),
                        ("DoUuTien", ASCENDING),
                    ],
                    {
                        "name": "idx_goiy_ketqua_uutien",
                    },
                )
            ],
            "LOG_ADMIN": [
                (
                    [
                        ("MaADM", ASCENDING),
                        ("ThoiDiemThucHien", ASCENDING),
                    ],
                    {
                        "name": "idx_logadmin_admin_time",
                    },
                )
            ],
            "LOG_KH": [
                (
                    [
                        ("MaKH", ASCENDING),
                        ("ThoiDiemThucHien", ASCENDING),
                    ],
                    {
                        "name": "idx_logkh_khachhang_time",
                    },
                )
            ],
        }

        # =============================================================
        # TẠO COLLECTION, INDEX VÀ UPSERT DỮ LIỆU
        # =============================================================

        existing_collections = await db.list_collection_names()

        for item in collections:
            collection_name = item["name"]
            documents = item.get("documents", [])

            if collection_name not in existing_collections:
                await db.create_collection(collection_name)
                print(f"Created collection: {collection_name}")
            else:
                print(f"Collection already exists: {collection_name}")

            collection = db[collection_name]

            # Tạo index
            for keys, options in indexes.get(collection_name, []):
                await collection.create_index(keys, **options)

            inserted_count = 0
            updated_count = 0

            # Dùng upsert để chạy script nhiều lần không bị trùng dữ liệu
            for document in documents:
                document_id = document["_id"]

                payload = {
                    key: value
                    for key, value in document.items()
                    if key != "_id"
                }

                result = await collection.update_one(
                    {"_id": document_id},
                    {"$set": payload},
                    upsert=True,
                )

                if result.upserted_id is not None:
                    inserted_count += 1
                elif result.modified_count > 0:
                    updated_count += 1

            print(
                f"Seeded {collection_name}: "
                f"inserted={inserted_count}, updated={updated_count}"
            )

        print(
            f"\nDatabase '{MONGODB_DB}' initialized successfully."
        )

    except Exception as error:
        print(f"MongoDB initialization failed: {error}")
        raise

    finally:
        # close() của Motor không phải hàm async
        client.close()


if __name__ == "__main__":
    asyncio.run(main())