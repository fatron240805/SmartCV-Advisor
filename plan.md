# SmartCV Advisor — Kế hoạch phát triển MVP

> **Tài liệu:** `plan.md`  
> **Phiên bản:** 1.1  
> **Ngày cập nhật:** 2026-07-16  
> **Trạng thái:** Sẵn sàng triển khai  
> **Mục tiêu:** Làm nguồn kế hoạch chính cho đội phát triển và AI coding agent.

---

## 1. Mục tiêu sản phẩm

SmartCV Advisor là nền tảng web SaaS tích hợp AI giúp sinh viên, người mới tốt nghiệp, fresher/junior và người đang tìm việc:

1. tải CV lên hệ thống;
2. trích xuất và chuẩn hóa nội dung CV;
3. chọn vị trí nghề nghiệp mục tiêu;
4. nhận điểm CV theo bộ tiêu chí và trọng số của vị trí đó;
5. xem lỗi phổ biến, điểm mạnh, điểm yếu và gợi ý cải thiện;
6. hiểu quyền lợi giữa tài khoản miễn phí và tài khoản Premium.

MVP phải chứng minh được giá trị cốt lõi: **người dùng biết CV hiện tại đang ở mức nào, vì sao bị trừ điểm và nên sửa gì tiếp theo**.

---

## 2. Thứ tự ưu tiên nguồn yêu cầu

Khi có mâu thuẫn giữa các tài liệu, áp dụng thứ tự sau:

1. **`Đặc tả Use Case - MVP (bổ sung)(1).csv`** — nguồn sự thật chính cho hành vi hệ thống, actor, luồng, business rule và NFR hiện tại.
2. **`main.pdf`** — nguồn sự thật cho tầm nhìn sản phẩm, khách hàng, giới hạn MVP và định hướng bảo mật dữ liệu CV.
3. **`Pipeline_CV_role_weighted.ipynb`** — prototype tham khảo cho pipeline trích xuất, chuẩn hóa section, role-weighted scoring và gợi ý.
4. **`N7_Agents.md`** — mẫu phương pháp tổ chức tài liệu, quy tắc làm việc và quy trình phát triển theo từng bước.
5. **Quyết định kỹ thuật mới nhất của dự án** — được ghi trực tiếp trong tài liệu này và có quyền thay thế giả định cũ trong báo cáo.

### Quyết định stack hiện tại

| Lớp | Công nghệ chính |
|---|---|
| Frontend | React + Vite + Tailwind CSS |
| Backend | Python 3.11+ + FastAPI |
| Database | MongoDB |
| ODM/driver | PyMongo hoặc Motor; ưu tiên lớp repository rõ ràng |
| AI integration | API AI qua adapter, cấu hình bằng biến môi trường |
| Xử lý PDF | PyMuPDF |
| Xử lý DOCX | `python-docx` |
| OCR scan/ảnh CV | GPT image model qua OpenAI API; không dùng OCR cục bộ |
| Validation | Pydantic |
| Authentication | JWT access token ngắn hạn + refresh token có kiểm soát |
| Deployment | Frontend trên Vercel; backend trên Render hoặc nền tảng tương đương; MongoDB Atlas |

> Báo cáo ban đầu có nhắc Supabase. Kế hoạch triển khai hiện tại dùng **MongoDB** theo quyết định kỹ thuật mới nhất của dự án. Không tự ý quay lại Supabase nếu chưa có quyết định thay đổi.

---

## 3. Phạm vi MVP

### 3.1. Trong phạm vi

#### Nhóm Admin

| UC | Chức năng |
|---|---|
| UC-001 | Quản lý danh sách Role IT |
| UC-002 | Quản lý điểm số/trọng số skill theo Role IT |
| UC-004 | Quản lý người dùng |

#### Nhóm tài khoản

| UC | Chức năng |
|---|---|
| UC-008 | Đăng ký |
| UC-009 | Đăng nhập |
| UC-010 | Đăng xuất |
| UC-011 | Quản lý thông tin cá nhân và yêu cầu xóa dữ liệu |

#### Nhóm phân tích CV

| UC | Chức năng |
|---|---|
| UC-012 | Tải CV PDF/DOC/DOCX, kiểm tra tệp và ghi nhận đồng ý xử lý dữ liệu |
| UC-013 | Chọn ngành nghề hoặc vị trí mục tiêu |
| UC-014 | Trích xuất, phân tích và chấm điểm CV |
| UC-015 | Xem điểm tổng quan, điểm thành phần và lỗi cơ bản |
| UC-016 | Xem gợi ý cải thiện theo quyền Registered/Premium |
| UC-024 | Xem lịch sử phân tích theo quyền tài khoản, mở lại chi tiết và xóa kết quả |
| UC-026 | Xem gói dịch vụ và trạng thái gói hiện tại |

### 3.2. Ngoài phạm vi MVP hiện tại

Các chức năng sau chỉ triển khai khi có use case hoặc quyết định mở rộng chính thức:

- so khớp CV với một JD cụ thể;
- Matching Score CV–JD;
- Keyword Gap dựa trên JD;
- Skill Gap chuyên sâu và roadmap 1 tuần/1 tháng/3 tháng;
- AI Chat chỉnh CV theo hội thoại;
- trình biên tập CV trực tiếp;
- tải CV đã chỉnh sửa;
- thanh toán thật;
- B2B/B2B2C cho trường học, trung tâm đào tạo hoặc nền tảng tuyển dụng;
- fine-tune mô hình riêng;
- phân tích hàng loạt nhiều CV.

Trang gói dịch vụ có thể hiển thị các tính năng tương lai để truyền thông, nhưng các tính năng chưa triển khai phải được đánh dấu rõ là **chưa khả dụng** hoặc **sắp ra mắt**, không tạo cảm giác hệ thống đã hỗ trợ.

**Cách áp dụng UC-024 mà không mở rộng sai phạm vi:** lịch sử phân tích chỉ hiển thị dữ liệu thực sự đã được pipeline MVP tạo ra, như tên CV, thời gian, vị trí mục tiêu, điểm CV, điểm ATS nếu có trong kết quả hiện tại và trạng thái phân tích. Các trường Matching Score, Keyword Gap, Skill Gap, Roadmap, phiên bản CV đã chỉnh sửa hoặc hành động AI chỉ là trường mở rộng cho giai đoạn sau; MVP không tự tạo, không hiển thị như đã khả dụng và không thêm luồng sử dụng giả.

---

## 4. Nguyên tắc kiến trúc

### 4.1. Luồng tổng thể

```text
React/Vite Frontend
        |
        | HTTPS / REST
        v
FastAPI Backend
  |-- Auth & RBAC
  |-- User/Profile
  |-- Role/Skill Configuration
  |-- CV Upload & Consent
  |-- Document Extraction
  |-- AI Analysis Orchestrator
  |-- Deterministic Scoring Engine
  |-- Result/Suggestion Service
  |-- Analysis History & Entitlement Service
  |-- Admin/Audit Log
        |
        +--> MongoDB
        +--> AI Provider Adapter
        +--> Temporary/File Storage Layer
```

### 4.2. Nguyên tắc tách trách nhiệm

- **AI không được tự quyết định toàn bộ điểm số.** AI dùng để nhận diện section, trích xuất bằng chứng, phát hiện lỗi ngữ nghĩa và tạo nhận xét.
- **Backend tính điểm cuối cùng** dựa trên cấu hình section, skill, trọng số và phiên bản scoring rule.
- Mọi kết quả phải truy vết được đến:
  - Role đã chọn;
  - phiên bản cấu hình chấm điểm;
  - bằng chứng trong CV;
  - thời điểm phân tích;
  - model/prompt version đã sử dụng.
- Frontend chỉ hiển thị dữ liệu; không chứa công thức chấm điểm nghiệp vụ quan trọng.
- Tất cả secret, API key và connection string nằm trong biến môi trường; không commit vào Git.

---

## 5. Thiết kế pipeline phân tích CV

### 5.1. Các bước xử lý

1. **Upload validation**
   - chỉ nhận `.pdf`, `.doc`, `.docx` và ảnh CV `.png`, `.jpg`, `.jpeg`, `.webp`, `.bmp`;
   - tối đa 5 MB cho Registered User;
   - kiểm tra MIME type, extension, file signature và khả năng đọc;
   - ghi nhận consent trước khi lưu/xử lý.

2. **Document extraction**
   - PDF có text layer: PyMuPDF;
   - PDF scan: render trang bằng PyMuPDF và dùng GPT image model qua OpenAI API để OCR/tách section;
   - DOCX: `python-docx`;
   - ảnh CV: dùng GPT image model qua OpenAI API để OCR/tách section;
   - `.doc`: chuyển đổi qua dịch vụ/tiện ích an toàn hoặc từ chối có hướng dẫn nếu môi trường không hỗ trợ ổn định.

3. **Text normalization**
   - chuẩn hóa khoảng trắng và ký tự;
   - giữ nguyên bằng chứng như tên công nghệ, dự án, công ty, mốc thời gian và số liệu;
   - không tự thêm thông tin không có trong CV.

4. **Section parsing**
   - `Professional Summary`;
   - `Education`;
   - `Experience`;
   - `Projects`;
   - `Technical Skills`;
   - `Certifications`;
   - `Other`.

5. **Evidence extraction**
   - kỹ năng xuất hiện ở section nào;
   - evidence level;
   - mốc thời gian;
   - số liệu/impact;
   - công nghệ và ngữ cảnh sử dụng;
   - lỗi, dữ liệu thiếu hoặc mâu thuẫn tiềm năng.

6. **Role-weighted scoring**
   - lấy cấu hình Role và Skill đang hoạt động;
   - tính điểm bằng scoring engine phía backend;
   - lưu `scoring_config_version` để không hồi tố kết quả cũ.

7. **Feedback generation**
   - điểm mạnh;
   - điểm yếu;
   - lỗi phổ biến;
   - gợi ý cơ bản cho Registered;
   - giải thích chi tiết/câu mẫu giới hạn cho Premium;
   - không bịa thành tích, kinh nghiệm hoặc kỹ năng.

8. **Persistence and presentation**
   - lưu kết quả có cấu trúc và gắn duy nhất với `analysis_id`;
   - lưu snapshot quyền/gói tại thời điểm phân tích để giải thích dữ liệu lịch sử;
   - cập nhật trạng thái job;
   - frontend poll hoặc nhận trạng thái tiến trình;
   - tạo bản ghi có thể truy xuất trong lịch sử khi phân tích hoàn tất;
   - hiển thị kết quả trong tối đa 30 giây theo NFR.

### 5.2. Trọng số section ban đầu

| Section | Điểm tối đa |
|---|---:|
| Professional Summary | 10 |
| Education | 10 |
| Experience | 20 |
| Projects | 15 |
| Technical Skills | 35 |
| Certifications | 10 |
| **Tổng** | **100** |

Các trọng số này là baseline từ prototype. Trước khi demo chính thức, cần đối chiếu với cấu hình quản trị và chuyên gia HR. Không dùng công thức hiệu chỉnh tùy ý như nhân hệ số toàn bài nếu chưa được mô tả trong business rule.

### 5.3. Mức độ quan trọng của skill

| Giá trị | Ý nghĩa |
|---:|---|
| 0 | Không dùng để chấm role này |
| 1 | Nice to have |
| 2 | Quan trọng |
| 3 | Rất quan trọng/bắt buộc |

### 5.4. Evidence level

| Mức | Diễn giải |
|---:|---|
| 0 | Không phát hiện |
| 1 | Chỉ nhắc mơ hồ |
| 2 | Liệt kê rõ trong Skills/Education/Certification |
| 3 | Có bằng chứng trong Experience/Project với ngữ cảnh cụ thể |

### 5.5. Kiểm tra mâu thuẫn

MVP hỗ trợ cảnh báo mềm cho các trường hợp như:

- số năm kinh nghiệm vượt quá thời gian có thể suy ra từ học tập/làm việc;
- một kỹ năng xuất hiện nhưng không có bằng chứng ở project/experience;
- mốc thời gian chồng chéo hoặc không hợp lý;
- tiêu đề vị trí không khớp mô tả công việc;
- thành tích có số liệu nhưng thiếu ngữ cảnh.

Cảnh báo phải dùng ngôn ngữ trung lập: **“Có thể có mâu thuẫn, vui lòng kiểm tra lại”**, không kết luận người dùng gian dối.

---

## 6. Mô hình dữ liệu MongoDB dự kiến

### 6.1. Collections chính

| Collection | Mục đích |
|---|---|
| `users` | tài khoản, role hệ thống, trạng thái, profile, subscription summary |
| `refresh_tokens` | refresh token đã hash, thiết bị, hạn dùng, trạng thái thu hồi |
| `career_roles` | Role IT, mô tả, trạng thái, ngày tạo/cập nhật |
| `skills` | danh mục kỹ năng dùng chung |
| `role_skill_configs` | kỹ năng, điểm/trọng số, mức quan trọng theo từng Role |
| `scoring_config_versions` | snapshot cấu hình chấm điểm theo phiên bản |
| `cv_documents` | metadata tệp, chủ sở hữu, consent, trạng thái, storage reference |
| `analysis_jobs` | trạng thái hàng đợi: pending/processing/completed/failed |
| `analysis_results` | section, evidence, score, lỗi, gợi ý, model/prompt/config version, snapshot gói và metadata lịch sử |
| `service_plans` | Free/Premium, giá, thời hạn, quyền lợi, trạng thái |
| `audit_logs` | log thao tác Admin và thay đổi cấu hình |
| `data_deletion_requests` | yêu cầu xóa dữ liệu và trạng thái xử lý |

### 6.2. Quy tắc dữ liệu bắt buộc

- Email unique theo dạng lowercase normalized.
- Role nghề nghiệp unique không phân biệt hoa thường.
- Role đã có lịch sử phân tích không xóa cứng; chuyển trạng thái inactive.
- Thay đổi role/skill config chỉ áp dụng cho phân tích mới.
- Tài khoản Premium còn hiệu lực không xóa cứng; khóa hoặc xử lý theo chính sách dữ liệu.
- Mọi kết quả phân tích phải chứa `analysis_id`, `user_id`, `cv_id`, `career_role_id`, `scoring_config_version`, `created_at`, `status` và snapshot gói tại thời điểm phân tích.
- Lịch sử mặc định sắp xếp theo `created_at` giảm dần; mỗi mục phải truy vết được về đúng `analysis_id`.
- Registered User được xem số kết quả gần nhất theo cấu hình `FREE_HISTORY_LIMIT` (mặc định 3, có thể cấu hình trong khoảng 3–5); Premium User được xem toàn bộ lịch sử còn tồn tại.
- Khi Premium hết hạn, quyền xem quay về mức Registered; kết quả cũ không bị xóa, các mục vượt giới hạn chuyển sang trạng thái khóa.
- Tìm kiếm lịch sử hỗ trợ tên CV và khoảng ngày; danh sách dài phải phân trang/cursor.
- Xóa một mục lịch sử phải có xác nhận, chỉ tác động đến kết quả thuộc người dùng hiện tại và không tự xóa tệp CV gốc nếu người dùng chưa yêu cầu xóa dữ liệu CV.
- Mọi truy vấn CV/result/history phải lấy `user_id` từ phiên xác thực và kiểm tra ownership; không tin `user_id` do client gửi.
- Dữ liệu lịch sử phải truyền qua TLS, được mã hóa khi lưu trữ theo năng lực của nền tảng database/storage và không xuất hiện trong log ứng dụng.

### 6.3. Index phục vụ UC-024

```text
analysis_results(user_id, created_at desc)
analysis_results(user_id, cv_filename_normalized)
analysis_results(user_id, status, created_at desc)
```

Các truy vấn lịch sử phải luôn bắt đầu bằng điều kiện `user_id` lấy từ phiên xác thực. Tìm kiếm tên CV nên dùng trường đã chuẩn hóa và giới hạn kiểu tìm kiếm để index có thể hỗ trợ; không quét toàn bộ collection rồi lọc ở frontend.

---

## 7. API dự kiến

### 7.1. Authentication và profile

```text
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh
POST   /api/v1/auth/logout
POST   /api/v1/auth/forgot-password
POST   /api/v1/auth/reset-password
GET    /api/v1/users/me
PATCH  /api/v1/users/me
POST   /api/v1/users/me/data-deletion-request
```

### 7.2. Role và skill

```text
GET    /api/v1/career-roles
GET    /api/v1/career-roles/{role_id}

GET    /api/v1/admin/career-roles
POST   /api/v1/admin/career-roles
PATCH  /api/v1/admin/career-roles/{role_id}
PATCH  /api/v1/admin/career-roles/{role_id}/status

GET    /api/v1/admin/career-roles/{role_id}/skills
POST   /api/v1/admin/career-roles/{role_id}/skills
PATCH  /api/v1/admin/career-roles/{role_id}/skills/{config_id}
PATCH  /api/v1/admin/career-roles/{role_id}/skills/bulk
```

### 7.3. CV và phân tích

```text
POST   /api/v1/cvs
GET    /api/v1/cvs/{cv_id}
DELETE /api/v1/cvs/{cv_id}
POST   /api/v1/cvs/{cv_id}/analyses
GET    /api/v1/analyses
GET    /api/v1/analyses/{analysis_id}/status
GET    /api/v1/analyses/{analysis_id}
GET    /api/v1/analyses/{analysis_id}/suggestions
DELETE /api/v1/analyses/{analysis_id}
```

`GET /api/v1/analyses` phục vụ UC-024 và hỗ trợ `search`, `date_from`, `date_to`, `cursor/page` và `limit`. Backend phải áp dụng giới hạn Free/Premium trước khi trả dữ liệu; response nên có metadata như `access_level`, `visible_count`, `locked_count` và `next_cursor`. Trường của các tính năng tương lai chỉ được trả khi bản ghi thật sự có dữ liệu và tính năng đó đã được bật.

### 7.4. Admin user và service plans

```text
GET    /api/v1/admin/users
GET    /api/v1/admin/users/{user_id}
PATCH  /api/v1/admin/users/{user_id}
POST   /api/v1/admin/users/{user_id}/lock
POST   /api/v1/admin/users/{user_id}/unlock

GET    /api/v1/service-plans
GET    /api/v1/service-plans/{plan_id}
```

---

## 8. Cấu trúc thư mục đề xuất

```text
smartcv-advisor/
├─ frontend/
│  ├─ src/
│  │  ├─ app/
│  │  ├─ components/
│  │  ├─ features/
│  │  │  ├─ auth/
│  │  │  ├─ profile/
│  │  │  ├─ cv-upload/
│  │  │  ├─ analysis/
│  │  │  ├─ results/
│  │  │  ├─ history/
│  │  │  ├─ plans/
│  │  │  └─ admin/
│  │  ├─ hooks/
│  │  ├─ lib/
│  │  ├─ services/
│  │  └─ types/
│  └─ .env.example
├─ backend/
│  ├─ app/
│  │  ├─ api/v1/
│  │  ├─ core/
│  │  ├─ models/
│  │  ├─ schemas/
│  │  ├─ repositories/
│  │  ├─ services/
│  │  │  ├─ auth/
│  │  │  ├─ documents/
│  │  │  ├─ ai/
│  │  │  ├─ scoring/
│  │  │  ├─ history/
│  │  │  └─ audit/
│  │  ├─ prompts/
│  │  └─ main.py
│  ├─ tests/
│  └─ .env.example
├─ docs/
├─ plan.md
├─ skills.md
└─ README.md
```

---

## 9. Kế hoạch triển khai theo milestone

### M0 — Bảo mật nguồn và khởi tạo nền tảng

**Mục tiêu:** tạo baseline an toàn trước khi phát triển.

- [ ] Thu hồi/rotate API key từng bị ghi trực tiếp trong notebook.
- [ ] Xóa secret khỏi notebook và lịch sử Git nếu đã commit.
- [ ] Tạo `.env.example`, `.gitignore` và quy ước biến môi trường.
- [ ] Khởi tạo cấu trúc frontend/backend.
- [ ] Cấu hình formatter, lint, type checking và test runner.
- [ ] Thiết lập kết nối MongoDB bằng repository layer.
- [ ] Tạo health check `/api/v1/health`.

**Tiêu chí hoàn thành**

- Không còn secret trong source code.
- Frontend và backend chạy được local.
- Backend kết nối MongoDB và trả health check thành công.

---

### M1 — Authentication và profile

**Use case:** UC-008, UC-009, UC-010, UC-011.

- [ ] Đăng ký với email, mật khẩu, xác nhận điều khoản.
- [ ] Hash mật khẩu bằng thuật toán phù hợp.
- [ ] Bỏ qua xác thực email trong MVP; tài khoản Registered được kích hoạt ngay sau khi đăng ký.
- [ ] Đăng nhập, khóa tạm 15 phút sau 5 lần sai.
- [ ] Access/refresh token, remember me và revoke token khi logout.
- [ ] Trang Profile và cập nhật thông tin được phép.
- [ ] Yêu cầu xóa dữ liệu.
- [ ] RBAC: Registered, Premium, Admin.

**Tiêu chí hoàn thành**

- Đăng ký ≤ 3 giây trong môi trường demo.
- Đăng nhập ≤ 2 giây.
- Logout hoàn tất gần như tức thì.
- Tài khoản bị khóa không sử dụng được token cũ.

---

### M2 — Admin quản lý Role và Skill scoring

**Use case:** UC-001, UC-002.

- [x] CRUD mềm cho Role IT.
- [x] Tìm kiếm/lọc Role.
- [x] Không cho xóa cứng Role đã có kết quả phân tích.
- [x] Quản lý danh sách skill theo Role.
- [x] Chỉnh điểm, trọng số, mức quan trọng và mô tả tiêu chí.
- [x] Chỉnh sửa hàng loạt.
- [x] Validate số dương, giới hạn trọng số và quy tắc tổng trọng số.
- [x] Tạo snapshot `scoring_config_version` sau mỗi thay đổi có hiệu lực.
- [x] Audit log cho thêm/sửa/ngưng hoạt động.

**Tiêu chí hoàn thành**

- Tìm kiếm/lọc phản hồi dưới 1 giây với dữ liệu demo.
- Cấu hình mới không làm thay đổi kết quả phân tích cũ.
- Mọi thao tác Admin quan trọng có audit log.

---

### M3 — Upload CV và consent

**Use case:** UC-012, UC-013.

- [ ] Drag-and-drop và file picker.
- [ ] Validate extension, MIME, file signature, dung lượng và khả năng đọc.
- [ ] Hiển thị metadata file trước khi upload.
- [ ] Bắt buộc đồng ý xử lý dữ liệu CV.
- [ ] Ghi nhận version chính sách, thời gian và user.
- [ ] Lưu CV theo ownership; không cho user khác truy cập.
- [ ] Chọn/search Role mục tiêu.
- [ ] Hỗ trợ trạng thái Role inactive và giới hạn theo gói nếu áp dụng.

**Tiêu chí hoàn thành**

- File sai định dạng hoặc >5 MB bị từ chối đúng thông báo.
- Không thể upload khi chưa đồng ý xử lý dữ liệu.
- Upload file 2 MB đạt mục tiêu ≤ 5 giây trong môi trường demo ổn định.
- Danh sách Role hiển thị sau tương tác ≤ 0,5 giây.

---

### M4 — Document extraction và AI analysis core

**Use case:** UC-014.

- [ ] Trích xuất PDF text layer.
- [ ] Trích xuất DOCX.
- [ ] GPT image OCR cho PDF scan và ảnh CV.
- [ ] Chuẩn hóa 7 section.
- [ ] Structured output bằng Pydantic schema.
- [ ] Evidence extraction cho skill, project, impact và timeline.
- [ ] Deterministic scoring engine.
- [ ] Phát hiện mâu thuẫn ở mức cảnh báo mềm.
- [ ] Retry, timeout và fallback khi AI provider lỗi.
- [ ] Lưu model version, prompt version và config version.

**Tiêu chí hoàn thành**

- Pipeline trả kết quả có cấu trúc, không phụ thuộc vào markdown tự do.
- Tổng điểm luôn trong 0–100.
- Cùng một evidence/config tạo ra điểm số ổn định.
- Thời gian toàn trình mục tiêu ≤ 30 giây cho tệp hợp lệ.

---

### M5 — Trang kết quả, gợi ý và lịch sử phân tích

**Use case:** UC-015, UC-016, UC-024.

- [ ] Điểm tổng quan và xếp loại.
- [ ] Điểm theo section.
- [ ] Danh sách lỗi cơ bản và bằng chứng liên quan.
- [ ] Điểm mạnh, điểm yếu và hành động ưu tiên.
- [ ] Registered: checklist/gợi ý tổng quan.
- [ ] Premium: giải thích chi tiết và câu mẫu có nút Copy.
- [ ] Locked state và CTA nâng cấp cho nội dung Premium.
- [ ] Empty/error state khi result không tồn tại hoặc suggestion lỗi.
- [ ] Trang lịch sử hiển thị tên CV, thời gian, Role mục tiêu, điểm tổng quan, ATS Score nếu có và trạng thái phân tích.
- [ ] Sắp xếp mới nhất trước; tìm kiếm theo tên CV hoặc khoảng ngày; hỗ trợ phân trang/cursor.
- [ ] Registered chỉ xem số mục gần nhất theo `FREE_HISTORY_LIMIT`; Premium xem toàn bộ; hết hạn Premium thì các mục vượt giới hạn chuyển sang khóa.
- [ ] Mở chi tiết lịch sử bằng `analysis_id` và dùng lại màn hình kết quả hiện có.
- [ ] Xóa kết quả có hộp thoại xác nhận, cập nhật danh sách và kiểm tra ownership ở backend.
- [ ] Empty state “Bạn chưa có kết quả phân tích nào”, error state tải lại và CTA “Phân tích CV ngay”.
- [ ] Chuẩn bị resource text tiếng Việt/tiếng Anh cho màn hình lịch sử.
- [ ] Không hiển thị Matching Score, Keyword Gap, Skill Gap, Roadmap, AI Assistant hoặc CV đã chỉnh sửa nếu MVP chưa tạo các dữ liệu này.

**Tiêu chí hoàn thành**

- Trang result tải dữ liệu đã có dưới 1 giây trong môi trường demo.
- Danh sách lịch sử phản hồi trong vòng 3 giây với dữ liệu demo và phân trang đúng.
- Registered không thể lấy các mục vượt giới hạn bằng cách gọi API trực tiếp; Premium hết hạn được hạ quyền ngay.
- User A không xem hoặc xóa được lịch sử của User B.
- Registered không truy cập được nội dung Premium qua API trực tiếp.
- Gợi ý không thêm thông tin không tồn tại trong CV.
- Mỗi lỗi có mô tả dễ hiểu và hành động sửa cụ thể.

---

### M6 — Service plans và Admin user management

**Use case:** UC-004, UC-026.

- [ ] Danh sách Free/Premium từ database.
- [ ] Guest được xem plans.
- [ ] Registered thấy plan hiện tại và CTA nâng cấp.
- [ ] Premium thấy trạng thái, ngày hết hạn và CTA gia hạn.
- [x] Admin xem, tìm kiếm, lọc và phân trang user.
- [x] Admin khóa/mở khóa user với lý do và xác nhận.
- [x] Force logout khi user bị khóa.
- [x] Không cho Admin thường khóa Admin khác.

**Tiêu chí hoàn thành**

- Trang plans tải ≤ 3 giây.
- Danh sách user phân trang tối đa 50 dòng/trang và tải ≤ 2 giây.
- Khóa tài khoản làm mất hiệu lực phiên hiện tại.

---

### M7 — Kiểm thử, bảo mật, deployment và demo

- [ ] Unit test scoring engine.
- [ ] Unit test validation file và RBAC.
- [ ] Integration test auth, upload, analysis, result và history.
- [ ] E2E happy path từ đăng ký đến xem kết quả, mở lại lịch sử và xóa một kết quả.
- [ ] Test IDOR: user A không xem/xóa được CV, result hoặc history của user B.
- [ ] Test prompt injection trong nội dung CV.
- [ ] Test file độc hại/không đúng MIME.
- [ ] Rate limit cho auth, upload và analysis.
- [ ] Log có cấu trúc nhưng không ghi raw CV hoặc secret.
- [ ] Deploy frontend, backend và database.
- [ ] Chuẩn bị seed data Role/Skill và tài khoản demo.
- [ ] Viết README chạy local và checklist demo.

**Tiêu chí hoàn thành**

- Không có lỗi blocker/critical.
- E2E happy path chạy ổn định.
- Không lộ secret hoặc dữ liệu CV trong log.
- Demo có dữ liệu seed và có thể reset an toàn.

---

## 10. Ma trận truy vết Use Case → Milestone

| Use case | Milestone | Trạng thái |
|---|---|---|
| UC-001 Quản lý Role IT | M2 | Đã triển khai |
| UC-002 Quản lý điểm skill | M2 | Đã triển khai |
| UC-004 Quản lý người dùng | M6 | Đã triển khai |
| UC-008 Đăng ký | M1 | Chưa bắt đầu |
| UC-009 Đăng nhập | M1 | Chưa bắt đầu |
| UC-010 Đăng xuất | M1 | Chưa bắt đầu |
| UC-011 Quản lý thông tin cá nhân | M1 | Chưa bắt đầu |
| UC-012 Tải CV | M3 | Chưa bắt đầu |
| UC-013 Chọn Role mục tiêu | M3 | Chưa bắt đầu |
| UC-014 Phân tích và chấm điểm | M4 | Chưa bắt đầu |
| UC-015 Xem kết quả | M5 | Chưa bắt đầu |
| UC-016 Xem gợi ý | M5 | Chưa bắt đầu |
| UC-024 Xem lịch sử phân tích | M5 | Chưa bắt đầu |
| UC-026 Xem gói dịch vụ | M6 | Chưa bắt đầu |

---

## 11. Chiến lược kiểm thử

### 11.1. Test dữ liệu CV

Bộ test tối thiểu cần có:

- PDF có text layer chuẩn;
- PDF scan;
- DOCX đơn giản;
- CV tiếng Việt;
- CV tiếng Anh;
- CV thiếu section;
- CV có bảng/cột;
- CV có nhiều kỹ năng nhưng không có bằng chứng;
- CV có project mạnh nhưng thiếu Technical Skills section;
- CV có timeline mâu thuẫn;
- file mã hóa, hỏng, sai MIME hoặc quá dung lượng.

### 11.2. Test scoring

- điểm section không âm và không vượt max;
- tổng điểm không vượt 100;
- skill importance 0 không ảnh hưởng điểm;
- thay đổi config tạo version mới;
- kết quả cũ giữ nguyên sau khi config thay đổi;
- evidence level cao phải có bằng chứng được trích dẫn từ CV;
- thiếu nhiều skill nice-to-have không được phạt nặng.

### 11.3. Test bảo mật

- password không lưu plaintext;
- refresh token lưu dạng hash;
- ownership check cho CV/result/history;
- giới hạn lịch sử Free/Premium được áp dụng ở backend;
- Premium hết hạn không còn lấy được mục lịch sử bị khóa;
- xóa lịch sử chỉ tác động đến dữ liệu của chính user;
- RBAC cho `/admin/*`;
- force logout sau khi khóa;
- không lộ raw CV trong error/log;
- prompt từ CV không thể thay đổi system instruction;
- kiểm soát loại và kích thước file;
- CORS chỉ cho origin được cấu hình.

---

## 12. Rủi ro và biện pháp giảm thiểu

| Rủi ro | Mức độ | Biện pháp |
|---|---|---|
| API key từng bị hard-code trong notebook | Critical | rotate key, xóa khỏi source và history, dùng `.env` |
| AI trả JSON sai schema | Cao | structured output, Pydantic validation, retry/fallback |
| Điểm số không ổn định | Cao | backend deterministic scoring, config versioning |
| AI bịa thông tin CV | Cao | evidence-only prompt, kiểm tra mọi gợi ý dựa trên source text |
| GPT OCR sai | Trung bình | chỉ dùng GPT OCR khi PDF thiếu text layer hoặc input là ảnh CV, hiển thị cảnh báo confidence thấp |
| File chứa dữ liệu cá nhân | Cao | consent, RBAC, retention, delete request, log tối thiểu |
| Chi phí AI tăng | Trung bình | giới hạn lượt, cache kết quả, model adapter, token budget |
| Người dùng hiểu điểm AI là quyết định tuyển dụng | Cao | disclaimer rõ ràng, giải thích tiêu chí và giới hạn |
| Lộ lịch sử của người dùng khác hoặc bypass giới hạn gói | Critical | lấy owner từ token, server-side entitlement, IDOR test, index theo owner |
| UC-024 nhắc dữ liệu của tính năng tương lai | Cao | chỉ hiển thị field thực sự tồn tại; giữ field tương lai optional và feature-gated |
| Cấu hình Admin làm sai tổng trọng số | Cao | validation, preview, versioning, audit log |
| Render cold start hoặc xử lý >30 giây | Trung bình | warm-up, timeout, async job, progress state |

---

## 13. Definition of Done cho một tính năng

Một tính năng chỉ được đánh dấu hoàn thành khi:

- [ ] bám đúng use case và không tự mở rộng phạm vi;
- [ ] có schema request/response rõ ràng;
- [ ] có xử lý quyền truy cập;
- [ ] có validation và error state;
- [ ] frontend kết nối API thật, không chỉ mock;
- [ ] có unit/integration test phù hợp;
- [ ] không chứa secret hoặc dữ liệu nhạy cảm trong code/log;
- [ ] đạt NFR liên quan hoặc có số đo và ghi chú chưa đạt;
- [ ] cập nhật `plan.md` và tài liệu liên quan;
- [ ] có tóm tắt file đã thay đổi và cách kiểm thử.

---

## 14. Quy tắc cập nhật tiến độ

Khi hoàn thành một milestone:

1. đổi checkbox từ `[ ]` sang `[x]`;
2. cập nhật trạng thái trong ma trận truy vết;
3. ghi ngày hoàn thành;
4. ghi test đã chạy;
5. ghi vấn đề còn tồn tại;
6. không xóa lịch sử quyết định quan trọng; thêm mục “Decision Log”.

### Decision Log

| Ngày | Quyết định | Lý do |
|---|---|---|
| 2026-07-16 | Dùng React/Vite/Tailwind + FastAPI + MongoDB | Đồng bộ với stack triển khai mới nhất của dự án |
| 2026-07-16 | AI chỉ trích xuất/nhận xét; backend tính điểm cuối | Tăng tính ổn định, giải thích được và kiểm thử được |
| 2026-07-16 | Chưa triển khai JD Matching/AI Chat/Roadmap trong core MVP | Bám giới hạn MVP và danh sách use case hiện tại |
| 2026-07-16 | Bổ sung UC-024 Lịch sử phân tích; Free xem giới hạn, Premium xem toàn bộ | Đồng bộ đặc tả hệ thống bổ sung nhưng không kích hoạt giả các tính năng tương lai |
| 2026-07-22 | Triển khai Admin UC-001/UC-002/UC-004 bằng API `/api/v1/admin/*` và giao diện Admin riêng | Bám đặc tả Admin, giữ cấu hình Role/Skill version hóa và kiểm tra RBAC ở backend |

