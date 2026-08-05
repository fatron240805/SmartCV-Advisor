# SmartCV Advisor

Ứng dụng web hỗ trợ phân tích CV theo vị trí IT mục tiêu: tải CV lên, hệ thống trích xuất nội dung, dùng GPT để đánh giá theo từng section và trả về điểm số, kỹ năng thiếu/đủ, lộ trình cải thiện.

## Tính năng chính

- Đăng ký/đăng nhập, xác thực email, quên mật khẩu qua SMTP (JWT access/refresh token).
- Tải CV (PDF/DOC/DOCX/ảnh), trích xuất nội dung bằng GPT (không cần OCR engine riêng).
- Phân tích CV theo vai trò IT: chấm điểm tổng quan, 5 tiêu chí, đánh giá kỹ năng, roadmap đề xuất.
- Lịch sử phân tích, gói dịch vụ Free/Premium.
- Trang quản trị (Admin): quản lý user, vai trò nghề nghiệp, cấu hình điểm kỹ năng, feedback, analytics.

## Công nghệ sử dụng

**Backend**: FastAPI, Motor/PyMongo (MongoDB), OpenAI API (GPT text + image model), PyJWT, PyMuPDF, python-docx.

**Frontend**: React 19 + TypeScript, Vite, React Router, Tailwind CSS, Axios.

## Cấu trúc thư mục

```
SmartCV-Advisor/
├─ backend/
│  ├─ app/
│  │  ├─ main.py              # Entry point FastAPI
│  │  ├─ db.py                # Kết nối MongoDB
│  │  ├─ routes/              # Định nghĩa API endpoints
│  │  ├─ services/            # Business logic (auth, cv, gpt, analysis...)
│  │  └─ data/                # Dataset vai trò/kỹ năng IT
│  ├─ tests/                  # Unit test (unittest)
│  └─ create_collections.py   # Script seed dữ liệu demo
└─ frontend/
   └─ src/
      ├─ pages/                # Các trang chính (Upload, Analysis, History...)
      ├─ components/
      ├─ services/api.ts       # Gọi API backend
      └─ types/
```

## Yêu cầu môi trường

- Python 3.12+
- Node.js + npm
- MongoDB (local hoặc Atlas)
- OpenAI API key

## Cài đặt & chạy

### 1. Backend

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Tạo file `backend/.env` với các biến tối thiểu:

```env
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=smartcv
JWT_SECRET_KEY=your_random_secret_key
FRONTEND_URL=http://localhost:5173
AUTH_SMTP_HOST=smtp.gmail.com
AUTH_SMTP_PORT=465
AUTH_SMTP_USER=your-sender@gmail.com
AUTH_SMTP_PASS=your-google-app-password
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini
OPENAI_IMAGE_MODEL=gpt-4o-mini
```

> Không commit `.env` hoặc API key lên Git.

Seed dữ liệu demo (user, vai trò IT, kỹ năng, gói dịch vụ):

```powershell
python create_collections.py
```

Chạy server:

```powershell
uvicorn app.main:app --reload --app-dir backend
```

Backend mặc định chạy tại `http://127.0.0.1:8000`.

### 2. Frontend

```powershell
cd frontend
npm install
npm run dev -- --host 127.0.0.1
```

Frontend mặc định chạy tại `http://127.0.0.1:5173`.

## API (tiền tố `/api/v1`)

| Nhóm | Prefix |
| --- | --- |
| Authentication | `/auth` |
| CV | `/cvs` |
| Career Roles | `/career-roles` |
| Analysis | `/analyses` |
| User Profile | `/users` |
| Service Plans | `/service-plans` |
| Feedback | `/feedback` |
| Analytics | `/analytics` |
| Admin | `/admin`, `/admin/plans`, `/admin/analytics` |

Kiểm tra tình trạng hệ thống (DB, SMTP, GPT): `GET /api/health`.

## Testing

```powershell
cd backend
python -m unittest discover tests
```

## Tài khoản demo (sau khi seed)

| Email | Mật khẩu | Vai trò |
| --- | --- | --- |
| `minhan@example.com` | `Demo1234` | Registered |
| `hoangnam@example.com` | `Demo1234` | Premium |
| `admin@smartcv.vn` | `Demo1234` | Admin |
