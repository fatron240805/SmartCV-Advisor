# SmartCV Advisor

SmartCV Advisor là MVP web app phân tích CV theo vị trí IT mục tiêu. Luồng hiện tại tập trung vào UC-012 đến UC-015:

1. Tải CV PDF/DOC/DOCX hoặc ảnh CV PNG/JPG/JPEG/WEBP/BMP và ghi nhận đồng ý xử lý dữ liệu.
2. Chọn vị trí mục tiêu.
3. Trích xuất nội dung CV, dùng GPT để tách section và review theo role.
4. Backend chuẩn hóa/cap điểm, lưu kết quả và hiển thị điểm tổng quan, 5 tiêu chí, lỗi cơ bản.

> Không commit `backend/.env`. API key GPT phải để trong `.env`, không hard-code trong code hoặc notebook.

## Yêu cầu môi trường

- Python 3.12+
- Node.js + npm
- MongoDB local hoặc MongoDB Atlas
- OpenAI API key
- Tesseract OCR và Poppler nếu muốn đọc ảnh CV hoặc PDF scan

## Cấu trúc chính

```text
SmartCV-Advisor/
├─ backend/
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ db.py
│  │  ├─ routes/
│  │  │  ├─ cv.py
│  │  │  ├─ analysis.py
│  │  │  └─ premium.py
│  │  └─ services/
│  │     ├─ cv_service.py
│  │     ├─ gpt_service.py
│  │     └─ analysis_service.py
│  ├─ create_collections.py
│  └─ .env.example
├─ frontend/
│  ├─ src/
│  │  ├─ App.tsx
│  │  ├─ pages/
│  │  │  ├─ UploadCvPage.tsx
│  │  │  ├─ AnalysisResultPage.tsx
│  │  │  ├─ HistoryPage.tsx
│  │  │  └─ PlansPage.tsx
│  │  └─ services/api.ts
│  └─ package.json
└─ README.md
```

## 1. Cấu hình backend

Mở terminal tại thư mục `backend`:

```powershell
cd D:\SmartCV-Advisor\backend
```

Tạo virtual environment nếu chưa có:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

Cài dependency:

```powershell
pip install fastapi "uvicorn[standard]" python-multipart python-dotenv openai pymupdf python-docx motor pymongo pillow pytesseract pdf2image
```

Để OCR ảnh/PDF scan giống notebook, máy cần có thêm Tesseract và Poppler:

- Tesseract Windows: cài từ bộ cài Tesseract OCR, rồi thêm thư mục cài đặt vào `PATH`.
- Poppler Windows: tải Poppler, giải nén và thêm thư mục `bin` vào `PATH`.
- Sau khi thêm `PATH`, đóng/mở lại terminal rồi chạy backend.

Tạo file `.env` từ mẫu:

```powershell
Copy-Item .env.example .env
```

Mở `backend/.env` và điền giá trị thật:

```env
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=smartcv
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
OPENAI_TIMEOUT_SECONDS=30
```

Nếu dùng MongoDB Atlas, thay `MONGODB_URI` bằng connection string Atlas. Nếu dùng key từng nằm trong notebook prototype, nên rotate/revoke key cũ rồi dán key mới vào `.env`.

## 2. Seed dữ liệu demo

Đảm bảo MongoDB chạy được, sau đó chạy:

```powershell
cd D:\SmartCV-Advisor\backend
.\.venv\Scripts\Activate.ps1
python create_collections.py
```

Script sẽ tạo dữ liệu mẫu:

- User demo `KH001`, `KH002`
- Role IT demo: Frontend, Backend
- CV demo `CV001`, `CV002`
- Kết quả demo `KQ001`
- Gói dịch vụ Free/Premium

## 3. Chạy backend

```powershell
cd D:\SmartCV-Advisor\backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Backend chạy tại:

- API: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/api/health`

API chính cho luồng CV:

| Method | Endpoint | Use case |
| --- | --- | --- |
| `POST` | `/api/v1/cvs` | UC-012 tải CV + consent |
| `GET` | `/api/v1/career-roles` | UC-013 chọn vị trí |
| `POST` | `/api/v1/cvs/{cv_id}/analyses` | UC-014 phân tích/chấm điểm |
| `GET` | `/api/v1/analyses/{analysis_id}` | UC-015 xem kết quả |
| `GET` | `/api/v1/analyses?limit=10` | Lịch sử demo |
| `GET` | `/api/v1/service-plans` | Gói dịch vụ |

## 4. Pipeline GPT đang chạy như thế nào

Pipeline backend lấy cảm hứng từ notebook `Pipeline_CV_role_weighted (1).ipynb`, nhưng đã tách thành service production hơn:

1. `cv_service.py`
   - Validate extension, MIME, signature, dung lượng 5 MB.
   - Đọc text PDF bằng PyMuPDF.
   - Nếu PDF gần như không có text layer (`<300` ký tự), dùng `pdf2image` + `pytesseract` để OCR giống notebook.
   - Đọc text DOCX bằng `python-docx`.
   - Đọc ảnh CV PNG/JPG/JPEG/WEBP/BMP bằng Pillow + `pytesseract`.
   - Gọi GPT để tách section chuẩn: `Professional Summary`, `Education`, `Experience`, `Projects`, `Technical Skills`, `Certifications`, `Other`.
   - Nếu không có `OPENAI_API_KEY` hoặc GPT lỗi, fallback sang rule-based section parser.

2. `gpt_service.py`
   - Đọc `OPENAI_API_KEY`, `OPENAI_MODEL`, `OPENAI_TIMEOUT_SECONDS` từ `.env`.
   - Gọi `client.chat.completions.create(...)` với `response_format={"type": "json_object"}` giống hướng notebook.
   - Prompt yêu cầu chỉ trả JSON, không markdown, không bịa thông tin ngoài CV.

3. `analysis_service.py`
   - Gọi GPT review section theo role/skill score.
   - Backend vẫn normalize/cap điểm theo 0-100 và lưu `scoring_config_version`.
   - Nếu GPT lỗi, fallback rule-based scoring để demo không bị dừng.
   - Lưu metadata: `ModelVersion`, `PromptVersion`, `AnalysisMethod`.

## 5. Chạy frontend

Mở terminal mới:

```powershell
cd D:\SmartCV-Advisor\frontend
npm install
npm run dev -- --host 127.0.0.1
```

Frontend chạy tại:

```text
http://127.0.0.1:5173
```

Các màn hình chính:

- Upload/analysis flow: `http://127.0.0.1:5173/upload`
- Kết quả demo: `http://127.0.0.1:5173/analysis/KQ001`
- Lịch sử: `http://127.0.0.1:5173/`
- Gói dịch vụ: `http://127.0.0.1:5173/plans`

Frontend đang gọi backend qua:

```ts
http://127.0.0.1:8000/api/v1
```

Cấu hình nằm trong `frontend/src/services/api.ts`.

## 6. Kiểm tra nhanh

Backend:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/api/health
Invoke-RestMethod http://127.0.0.1:8000/api/v1/career-roles
Invoke-RestMethod http://127.0.0.1:8000/api/v1/analyses/KQ001
```

Frontend:

```powershell
cd D:\SmartCV-Advisor\frontend
npm run build
npm run lint
```

## 7. Lỗi thường gặp

`OPENAI_API_KEY` chưa có hoặc sai:

- GPT parser/review sẽ fallback rule-based.
- Kiểm tra lại `backend/.env`.
- Restart backend sau khi sửa `.env`.

MongoDB không kết nối được:

- Kiểm tra `MONGODB_URI`.
- Nếu dùng Atlas, kiểm tra network/IP allowlist.
- Chạy lại `python create_collections.py` sau khi kết nối thành công.

Upload ảnh/PDF scan không đọc được:

- Kiểm tra đã cài Tesseract OCR và Poppler chưa.
- Kiểm tra Tesseract/Poppler đã nằm trong `PATH` của terminal chạy backend chưa.
- Dùng ảnh rõ nét, đủ sáng, không nghiêng nhiều.

Upload DOC cũ bị từ chối:

- `.doc` được validate signature nhưng hiện chưa đọc ổn định.
- Chuyển CV sang PDF, DOCX hoặc ảnh rõ nét.

Frontend không gọi được backend:

- Kiểm tra backend đang chạy ở port `8000`.
- Kiểm tra CORS trong `backend/app/main.py`.
- Mở Swagger `http://127.0.0.1:8000/docs` để test API trước.

## 8. Ghi chú bảo mật

- Không commit `backend/.env`.
- Không đưa OpenAI API key vào notebook, README, source code, screenshot hoặc log.
- Không log raw CV hoặc full prompt chứa nội dung CV.
- Nội dung CV chỉ nên gửi tối thiểu cần thiết cho GPT để phân tích.
