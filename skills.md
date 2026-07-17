# SmartCV Advisor — Skills và quy tắc làm việc cho AI Coding Agent

> **Tài liệu:** `skills.md`  
> **Phiên bản:** 1.1  
> **Ngày cập nhật:** 2026-07-16  
> **Mục đích:** Quy định những năng lực, quy trình và tiêu chuẩn mà AI coding agent phải áp dụng khi phân tích, thiết kế, code, kiểm thử hoặc cập nhật SmartCV Advisor.

---

## 1. Bối cảnh bắt buộc phải hiểu

SmartCV Advisor là web app tích hợp AI để phân tích CV theo vị trí nghề nghiệp mục tiêu. MVP hiện tại tập trung vào:

- quản lý Role IT và trọng số skill;
- đăng ký, đăng nhập, đăng xuất và profile;
- tải CV PDF/DOC/DOCX có consent;
- trích xuất và chuẩn hóa nội dung CV;
- chấm điểm theo Role;
- hiển thị kết quả, gợi ý cải thiện và lịch sử phân tích theo quyền tài khoản;
- phân quyền Registered/Premium;
- quản lý user phía Admin;
- hiển thị gói dịch vụ.

AI agent phải hiểu đây là **hệ thống hỗ trợ người dùng cải thiện hồ sơ**, không phải hệ thống ra quyết định tuyển dụng và không được khẳng định người dùng chắc chắn đậu/rớt.

---

## 2. Nguồn sự thật và cách xử lý mâu thuẫn

Trước mọi task, đọc theo thứ tự:

1. `skills.md`;
2. `plan.md`;
3. `Đặc tả Use Case - MVP (bổ sung)(1).csv`;
4. `main.pdf`;
5. `Pipeline_CV_role_weighted(2).ipynb`;
6. các file code hiện tại.

Nếu tài liệu xung đột:

- use case quyết định hành vi hệ thống;
- `plan.md` quyết định stack và phạm vi triển khai hiện tại;
- notebook chỉ là prototype tham khảo, không phải production architecture;
- không tự suy đoán; ghi rõ xung đột và chọn theo thứ tự ưu tiên trên.

---

## 3. Tech stack không được tự ý thay đổi

| Thành phần | Quy định |
|---|---|
| Frontend | React + Vite + Tailwind CSS |
| Backend | Python + FastAPI |
| Database | MongoDB |
| Validation | Pydantic |
| PDF | PyMuPDF |
| DOCX | `python-docx` |
| OCR | Tesseract, chỉ fallback |
| AI | qua provider adapter, secret từ environment |
| Testing frontend | Vitest + React Testing Library; E2E có thể dùng Playwright |
| Testing backend | Pytest + HTTPX/TestClient |

### Cấm

- tự đổi React sang Vue/Angular;
- tự đổi FastAPI sang Node/Express/Django;
- tự đổi MongoDB sang Supabase/Firebase/PostgreSQL;
- đưa Gradio vào production frontend;
- hard-code API key, JWT secret hoặc MongoDB URI;
- thêm dependency mới khi chưa chứng minh cần thiết;
- dùng AI để thay thế hoàn toàn scoring engine có quy tắc.

---

## 4. Các nguyên tắc không thương lượng

1. **Bám use case.** Triển khai UC-024 cho lịch sử phân tích, nhưng không tự kích hoạt JD Matching, Keyword Gap, Skill Gap, AI Chat, roadmap, CV chỉnh sửa hoặc thanh toán thật khi các module đó chưa thuộc MVP.
2. **Evidence-first.** Mọi đánh giá và gợi ý phải dựa trên nội dung có trong CV.
3. **Không bịa thông tin.** Không tự thêm kỹ năng, công ty, thành tích, số liệu hoặc thời gian.
4. **Điểm số phải giải thích được.** Mỗi điểm thành phần phải gắn với tiêu chí và bằng chứng.
5. **AI không tính điểm cuối một mình.** Backend áp dụng công thức deterministic từ config đã version hóa.
6. **Bảo vệ dữ liệu cá nhân.** CV, email, số điện thoại và kết quả phân tích là dữ liệu riêng tư.
7. **RBAC ở backend.** Ẩn nút trên UI không phải là kiểm soát quyền.
8. **Thay đổi config không hồi tố.** Kết quả cũ giữ nguyên `scoring_config_version`.
9. **Không log raw CV.** Chỉ log metadata cần thiết và correlation ID.
10. **Luôn kiểm thử trường hợp lỗi.** File hỏng, AI timeout, user bị khóa, result không tồn tại, quyền sai.

---

## 5. Skill 01 — Phân tích yêu cầu và truy vết Use Case

### Mục tiêu

Chuyển use case thành phạm vi triển khai rõ ràng mà không tự bịa chức năng.

### Khi sử dụng

- thêm màn hình;
- thêm endpoint;
- sửa luồng nghiệp vụ;
- thay đổi phân quyền;
- cập nhật business rule hoặc NFR.

### Quy trình

1. Xác định UC ID và actor.
2. Tóm tắt trigger, precondition, postcondition.
3. Tách basic flow, alternative flow, exception flow.
4. Liệt kê business rule và NFR liên quan.
5. Xác định dữ liệu cần đọc/ghi.
6. Xác định quyền truy cập.
7. Lập acceptance criteria có thể test.
8. Đối chiếu phạm vi trong `plan.md`.

### Đầu ra bắt buộc

```text
Use case:
Actor:
Scope:
Main flow:
Alternative/error flows:
Data changes:
API changes:
UI changes:
Security checks:
Acceptance criteria:
Out of scope:
```

### Tiêu chí chất lượng

- mỗi task phải truy ngược được về ít nhất một UC hoặc một quyết định kỹ thuật;
- không gộp nhiều thao tác khác nhau vào một basic flow nếu use case quy định một thao tác tiêu chuẩn;
- mọi exception quan trọng đều có UI state và API error tương ứng.

---

## 6. Skill 02 — Thiết kế UX cho luồng phân tích CV

### Mục tiêu

Thiết kế luồng rõ ràng, giảm tải nhận thức và giúp người dùng hiểu hệ thống đang làm gì.

### Nguyên tắc UX

- một màn hình chỉ có một primary action rõ ràng;
- hiển thị bước hiện tại: Upload → Chọn Role → Phân tích → Kết quả;
- trước upload phải hiển thị định dạng, dung lượng và consent;
- trong khi phân tích phải có progress/status và cách retry;
- điểm số phải đi kèm giải thích, không chỉ có biểu đồ;
- cảnh báo mâu thuẫn dùng ngôn ngữ trung lập;
- nội dung Premium bị khóa phải thể hiện rõ lý do và quyền lợi;
- không dark pattern ép nâng cấp;
- responsive trên desktop và mobile;
- trạng thái loading, empty, error và success phải được thiết kế đầy đủ;
- lịch sử phải sắp xếp mới nhất trước, hỗ trợ tìm theo tên CV/ngày và phân trang khi cần;
- mục vượt giới hạn Registered hiển thị trạng thái khóa rõ ràng, không dùng dark pattern;
- chi tiết lịch sử dùng lại trang kết quả theo `analysis_id`;
- chỉ hiển thị dữ liệu mà lần phân tích thực sự tạo ra; không dựng mock Matching/Gap/Roadmap như chức năng hoạt động.

### Checklist màn hình kết quả

- [ ] tổng điểm 0–100;
- [ ] xếp loại có mô tả;
- [ ] điểm từng section;
- [ ] lỗi và bằng chứng;
- [ ] điểm mạnh;
- [ ] hành động ưu tiên;
- [ ] disclaimer;
- [ ] locked state cho Premium;
- [ ] nút Copy cho câu mẫu Premium;
- [ ] retry khi suggestion lỗi;
- [ ] danh sách lịch sử, empty state và error state;
- [ ] locked state theo Free/Premium;
- [ ] tìm kiếm theo tên CV/ngày và pagination;
- [ ] hộp thoại xác nhận xóa kết quả.

---

## 7. Skill 03 — React/Vite/Tailwind Frontend

### Mục tiêu

Xây frontend theo feature, typed và dễ kiểm thử.

### Quy tắc triển khai

- component nhỏ, một trách nhiệm;
- tách server state khỏi local UI state;
- API call đi qua service/client chung;
- không gọi API trực tiếp rải rác trong component;
- dùng route guard cho UX nhưng vẫn dựa vào backend RBAC;
- form có client validation nhưng không thay backend validation;
- dùng design token/Tailwind config thay vì hard-code style lặp lại;
- không lưu access token nhạy cảm trong nơi dễ bị XSS nếu có phương án cookie an toàn;
- clear dữ liệu nhạy cảm khi logout;
- hỗ trợ cancel upload và abort request khi component unmount.

### Cấu trúc feature mẫu

```text
features/analysis/
├─ api/
├─ components/
├─ hooks/
├─ pages/
├─ schemas/
├─ types/
└─ utils/

features/history/
├─ api/
├─ components/
├─ hooks/
├─ pages/
├─ schemas/
├─ types/
└─ utils/
```

### Kiểm thử tối thiểu

- render trạng thái chính;
- validate form;
- unauthorized/forbidden state;
- upload sai định dạng;
- loading/error/success;
- Premium locked content;
- history Free/Premium entitlement;
- empty/search/pagination/delete history states;
- copy action.

---

## 8. Skill 04 — FastAPI Backend

### Mục tiêu

Xây API rõ ràng, an toàn và có khả năng kiểm thử độc lập.

### Quy tắc kiến trúc

```text
Router -> Service -> Repository -> MongoDB
                 -> AI Adapter
                 -> Scoring Engine
```

- router chỉ xử lý HTTP concern;
- service chứa business logic;
- repository chứa truy vấn database;
- schema Pydantic tách khỏi Mongo document nội bộ;
- dùng dependency injection cho auth, role và database;
- error response có `code`, `message`, `details`, `correlation_id`;
- tất cả endpoint có typing đầy đủ;
- không trả stack trace cho client;
- mọi endpoint Admin kiểm tra role ở backend;
- endpoint history lấy owner từ access token, không nhận `user_id` làm nguồn quyền;
- giới hạn Registered/Premium được áp dụng ở service/query backend trước khi serialize response;
- id từ client phải validate và xử lý not found.

### Chuẩn response gợi ý

```json
{
  "data": {},
  "meta": {},
  "error": null
}
```

### Chuẩn error gợi ý

```json
{
  "data": null,
  "error": {
    "code": "CV_FILE_TOO_LARGE",
    "message": "Dung lượng file quá lớn.",
    "details": {},
    "correlation_id": "..."
  }
}
```

---

## 9. Skill 05 — MongoDB Data Modeling

### Mục tiêu

Thiết kế dữ liệu phù hợp với truy vấn, versioning và audit.

### Quy tắc

- embed dữ liệu nhỏ, ổn định và luôn đọc cùng nhau;
- reference dữ liệu lớn, thay đổi độc lập hoặc cần audit/version;
- tạo index cho email, role name, user status, analysis owner và timestamps;
- dùng normalized fields để unique không phân biệt hoa thường;
- tránh document tăng vô hạn;
- dùng pagination cursor hoặc page/limit phù hợp;
- cập nhật cấu hình scoring bằng version snapshot;
- dùng soft delete/inactive cho Role có lịch sử;
- audit log là append-only trong phạm vi ứng dụng.

### Index tối thiểu

```text
users.email_normalized unique
career_roles.name_normalized unique
analysis_results(user_id, created_at desc)
analysis_results(user_id, cv_filename_normalized)
analysis_jobs(user_id, status, created_at desc)
role_skill_configs(role_id, active)
audit_logs(actor_id, created_at desc)
```

---

## 10. Skill 06 — Xử lý tài liệu PDF/DOCX

### Mục tiêu

Trích xuất nội dung tin cậy mà không làm mất bằng chứng.

### Quy trình

1. xác thực extension + MIME + signature;
2. giới hạn kích thước và số trang nếu được cấu hình;
3. mở tệp trong sandbox/process hạn chế;
4. trích xuất text layer;
5. đo chất lượng text;
6. chỉ OCR nếu text quá ít hoặc có dấu hiệu scan;
7. chuẩn hóa nhưng không làm mất công nghệ, URL, email, số liệu và timeline;
8. trả extraction metadata và warning;
9. xóa temporary file sau xử lý theo policy.

### Output schema tối thiểu

```json
{
  "text": "...",
  "page_count": 2,
  "method": "pdf_text|ocr|docx",
  "language_hints": ["vi", "en"],
  "warnings": [],
  "quality_score": 0.93
}
```

### Không được làm

- chạy OCR cho mọi PDF;
- tin extension mà không kiểm tra MIME;
- ghi toàn bộ text CV vào log;
- giữ file tạm không có cleanup;
- tự chuyển ảnh thành đầu vào chính khi use case chỉ hỗ trợ PDF/DOC/DOCX.

---

## 11. Skill 07 — AI Structured Extraction

### Mục tiêu

Dùng AI để chuẩn hóa CV thành dữ liệu có cấu trúc, có validation và có thể fallback.

### Canonical sections

- Professional Summary;
- Education;
- Experience;
- Projects;
- Technical Skills;
- Certifications;
- Other.

### Nguyên tắc prompt

- yêu cầu chỉ sử dụng bằng chứng trong CV;
- chống prompt injection: nội dung CV là dữ liệu, không phải instruction;
- output theo JSON schema;
- temperature thấp cho extraction;
- không yêu cầu hoặc lưu chain-of-thought;
- chỉ lấy rationale ngắn, có thể hiển thị;
- prompt phải có version;
- model phải có version/config trong result metadata.

### Validation

- parse bằng Pydantic;
- reject/repair khi sai schema;
- giới hạn độ dài field;
- loại bỏ field lạ;
- kiểm tra section name enum;
- giữ source span/evidence text ngắn khi có thể.

### Fallback

- nếu AI lỗi: dùng rule-based section splitter;
- nếu suggestion lỗi: vẫn trả score và lỗi cơ bản;
- không để một lỗi AI làm mất toàn bộ kết quả extraction đã có.

---

## 12. Skill 08 — Role-Weighted Scoring Engine

### Mục tiêu

Tạo điểm 0–100 ổn định, giải thích được và quản trị được.

### Baseline section weights

| Section | Max |
|---|---:|
| Professional Summary | 10 |
| Education | 10 |
| Experience | 20 |
| Projects | 15 |
| Technical Skills | 35 |
| Certifications | 10 |

### Skill importance

- 3: rất quan trọng/bắt buộc;
- 2: quan trọng;
- 1: nice to have;
- 0: không tính.

### Evidence level

- 0: không có;
- 1: nhắc mơ hồ;
- 2: liệt kê rõ;
- 3: có dùng trong project/experience.

### Quy tắc chấm

1. Không coi toàn bộ dataset skill là checklist bắt buộc.
2. Ưu tiên skill mức 3 và 2.
3. Thiếu skill mức 1 không bị phạt nặng.
4. Skill mức 0 không được đưa vào missing list.
5. Kỹ năng có evidence trong project/experience đáng tin hơn danh sách skill.
6. Điểm section phải cap tại max.
7. Tổng điểm cap 100.
8. Không dùng hệ số tùy ý như `raw_total * 1.5 + 4` nếu chưa được business rule phê duyệt.
9. Kết quả lưu kèm `scoring_config_version`.
10. Mỗi deduction/bonus phải có reason code và evidence.

### Output scoring tối thiểu

```json
{
  "total_score": 78.5,
  "classification": "Khá",
  "section_scores": [],
  "skill_assessment": [],
  "issues": [],
  "strengths": [],
  "priority_actions": [],
  "scoring_config_version": "..."
}
```

### Unit test bắt buộc

- min/max boundaries;
- missing sections;
- skill level 0;
- duplicate skill evidence;
- evidence ở nhiều section;
- config version khác nhau;
- CV ít skill nhưng bằng chứng mạnh;
- CV liệt kê nhiều skill nhưng không có bằng chứng.

---

## 13. Skill 09 — Feedback và Premium Content

### Mục tiêu

Tạo gợi ý hữu ích nhưng không bịa và đúng phân quyền.

### Registered

- checklist tổng quan;
- giải thích ngắn về lỗi;
- hành động tiếp theo ở mức định hướng;
- không hiển thị câu viết lại chi tiết bị khóa.

### Premium

- giải thích chi tiết;
- action verbs phù hợp;
- câu mẫu dựa trên dữ liệu có thật;
- cấu trúc STAR khi đủ dữ liệu;
- nút Copy;
- vẫn phải nói rõ phần nào người dùng cần tự bổ sung số liệu thật.

### Quy tắc câu mẫu

- dùng placeholder như `[số liệu thực tế]` nếu CV không có metric;
- không tự tạo phần trăm, số người dùng hoặc doanh thu;
- không nâng seniority;
- không đổi internship thành full-time;
- không biến coursework thành kinh nghiệm doanh nghiệp;
- không khẳng định chuẩn ATS tuyệt đối.

---

## 14. Skill 10 — Lịch sử phân tích và phân quyền gói

### Mục tiêu

Triển khai UC-024 để người dùng mở lại kết quả đã lưu mà không làm lộ dữ liệu, không bypass quyền gói và không biến các tính năng tương lai thành chức năng giả.

### Chính sách truy cập

- Registered User chỉ xem số kết quả gần nhất theo cấu hình `FREE_HISTORY_LIMIT`; mặc định 3 và chỉ cấu hình trong khoảng 3–5.
- Premium User xem toàn bộ lịch sử chưa bị xóa.
- Khi Premium hết hạn, quyền truy cập quay về Registered ngay; dữ liệu cũ vẫn được giữ nhưng các mục vượt giới hạn chuyển sang khóa.
- Quyền phải được kiểm tra ở backend trên từng request; không tải toàn bộ rồi chỉ ẩn bằng frontend.
- User chỉ xem và xóa kết quả của chính mình; `user_id` luôn lấy từ token/session.
- Mỗi mục lịch sử phải gắn với một `analysis_id` duy nhất.

### Dữ liệu và API

- sắp xếp mặc định `created_at DESC`;
- hỗ trợ tìm theo `cv_filename_normalized` và khoảng ngày;
- hỗ trợ cursor/page pagination;
- response có metadata `access_level`, `visible_count`, `locked_count`, `next_cursor`;
- snapshot tối thiểu: tên CV, Role mục tiêu, điểm CV, ATS Score nếu có, trạng thái, thời gian phân tích và trạng thái gói tại thời điểm phân tích;
- các field Matching Score, Keyword Gap, Skill Gap, Roadmap, AI rewrite/CV version là optional, chỉ trả khi module tương ứng thực sự tồn tại và được feature flag cho phép;
- xóa lịch sử cần xác nhận và chỉ xóa kết quả; không tự xóa CV gốc nếu người dùng chưa yêu cầu xóa dữ liệu CV.

### Trạng thái UI bắt buộc

- loading/skeleton;
- danh sách có dữ liệu;
- empty state “Bạn chưa có kết quả phân tích nào” và CTA “Phân tích CV ngay”;
- lỗi tải dữ liệu và nút thử lại;
- item bị khóa do giới hạn Free;
- detail not found hoặc không có quyền;
- confirm delete, delete success và delete failure;
- tài nguyên nội dung tiếng Việt và tiếng Anh cho màn hình lịch sử.

### NFR và bảo mật

- danh sách phản hồi trong vòng 3 giây ở tải mục tiêu;
- TLS khi truyền, mã hóa at-rest theo nền tảng;
- không log raw result, CV text hoặc PII;
- chống IDOR cho list/detail/delete;
- query phải dùng index theo owner và thời gian;
- không cho client tự đặt `plan_type` hoặc `premium=true`.

### Test bắt buộc

- Registered thấy đúng N mục mới nhất;
- Premium thấy toàn bộ;
- Premium hết hạn bị hạ quyền;
- user A không xem/xóa dữ liệu user B;
- sort mới nhất trước;
- search tên CV và khoảng ngày;
- pagination không trùng/mất mục;
- xóa rồi danh sách cập nhật;
- mục có field tương lai nhưng feature tắt thì không hiển thị;
- empty/error/locked state.

---

## 15. Skill 11 — Authentication, RBAC và Privacy

### Mục tiêu

Bảo vệ tài khoản và dữ liệu CV.

### Authentication

- password hash bằng Argon2id hoặc bcrypt cấu hình phù hợp;
- access token ngắn hạn;
- refresh token rotation hoặc revoke list;
- refresh token lưu hash;
- 5 lần sai → khóa 15 phút;
- logout thu hồi refresh token;
- khóa user → thu hồi mọi phiên;
- rate limit auth endpoints.

### RBAC

| Role | Quyền chính |
|---|---|
| Guest | xem landing/plans, đăng ký, đăng nhập |
| Registered | upload, phân tích, xem result/gợi ý cơ bản, profile và lịch sử giới hạn |
| Premium | quyền Registered + nội dung chi tiết và toàn bộ lịch sử được mở khóa |
| Admin | quản lý Role, Skill, User và audit data cần thiết |

### Privacy

- bắt buộc consent trước xử lý CV;
- lưu thời điểm và policy version;
- ownership check mọi CV/result/history;
- entitlement history được đánh giá từ trạng thái gói hiện tại;
- có cơ chế yêu cầu xóa dữ liệu;
- không dùng CV để train lại model khi chưa có đồng ý riêng;
- không log PII/raw CV;
- không gửi nhiều dữ liệu hơn cần thiết cho AI provider;
- mô tả retention policy trước production.

### Security incident bắt buộc xử lý

Notebook prototype có chứa API key dạng plaintext. Trước mọi tích hợp AI:

1. rotate/revoke key;
2. xóa key khỏi notebook;
3. kiểm tra Git history;
4. chuyển sang environment variable;
5. không lặp lại key trong issue, log hoặc chat.

---

## 16. Skill 12 — Testing và AI Evaluation

### Test pyramid

1. **Unit:** scoring, validation, normalization, permission helpers.
2. **Integration:** repository, auth, upload, AI adapter mock, result API, history list/detail/delete và entitlement.
3. **E2E:** đăng ký → login → upload → chọn Role → phân tích → xem result → mở lịch sử → mở lại/xóa kết quả.
4. **AI evaluation set:** CV mẫu có expected section/evidence/issues.

### Golden dataset tối thiểu

- 10 CV hợp lệ thuộc nhiều mức chất lượng;
- 2 CV scan;
- 2 CV song ngữ;
- 2 CV thiếu section;
- 2 CV có timeline mâu thuẫn;
- 2 CV cố gắng prompt injection;
- mỗi CV có expected output mức high-level, không cần exact wording.

### Chỉ số đánh giá

- section classification accuracy;
- skill evidence precision/recall;
- score stability cùng config;
- hallucination rate;
- JSON schema success rate;
- latency p50/p95;
- cost per analysis;
- user-rated usefulness của suggestion;
- history latency p50/p95;
- tỷ lệ lỗi authorization/IDOR bằng 0 trong test suite;
- độ đúng của Free/Premium entitlement và pagination.

### Quy tắc mock

- unit/integration test không gọi API AI thật;
- dùng fixture response đã validate;
- chỉ chạy live-model evaluation trong test suite riêng có budget và secret riêng.

---

## 17. Skill 13 — Deployment và Observability

### Mục tiêu

Triển khai có thể theo dõi mà không làm lộ dữ liệu.

### Yêu cầu

- environment riêng: local/staging/production;
- secret quản lý bởi nền tảng deployment;
- health/readiness endpoint;
- structured log với correlation ID;
- metrics: request count, error rate, latency, AI latency, token/cost estimate;
- không log request body của upload/analysis;
- timeout/retry/circuit breaker cho AI provider;
- CORS allowlist;
- file storage có cleanup;
- backup MongoDB và quy trình restore cho dữ liệu cấu hình;
- seed data demo tách production.

---

## 18. Quy trình bắt buộc khi phát triển một tính năng mới

AI coding agent phải đi qua đủ 8 bước. Không được nhảy thẳng vào code.

### Bước 1 — Scope check

- Tính năng thuộc UC nào?
- Có nằm trong MVP không?
- Có xung đột với giới hạn sản phẩm không?
- Với UC-024, field nào là dữ liệu MVP thật và field nào chỉ dành cho giai đoạn sau?
- Nếu ngoài phạm vi, dừng và nêu rõ.

### Bước 2 — Actor và quyền

- Guest, Registered, Premium hay Admin?
- Precondition và postcondition?
- Backend permission check nào cần có?

### Bước 3 — UX flow

- điểm bắt đầu;
- từng hành động người dùng;
- phản hồi hệ thống;
- loading/error/empty/success;
- điểm kết thúc.

### Bước 4 — Data và API design

- collection/field/index;
- request/response schema;
- endpoint;
- validation;
- audit/versioning.

### Bước 5 — Backend implementation

- repository;
- service;
- router;
- RBAC;
- error handling;
- tests.

### Bước 6 — Frontend implementation

- page/component;
- API integration;
- form state;
- responsive/accessibility;
- error state;
- tests.

### Bước 7 — Verification

- happy path;
- alternative flow;
- exception flow;
- security test;
- NFR measurement.

### Bước 8 — Documentation

- cập nhật `plan.md`;
- liệt kê file thay đổi;
- test đã chạy;
- giả định;
- phần chưa hoàn thiện;
- bước tiếp theo.

---

## 19. Quy tắc code quality

### Python

- type hints cho public function;
- Pydantic cho API boundary;
- async chỉ dùng khi thư viện và workload thực sự hỗ trợ;
- không dùng broad `except Exception` nếu có thể bắt lỗi cụ thể;
- không đặt business logic trong router;
- docstring cho scoring/extraction logic phức tạp;
- formatter/linter/type checker theo cấu hình dự án.

### React/TypeScript

- ưu tiên TypeScript;
- không dùng `any` tùy tiện;
- component props có type;
- không mutate state;
- không duplicate API types thủ công nếu có thể sinh/chia sẻ schema;
- xử lý abort/cancel cho request dài;
- aria label và keyboard interaction cho control quan trọng.

### Git

- commit nhỏ, một mục đích;
- không commit `.env`, file CV thật hoặc output chứa PII;
- không force-push nhánh dùng chung nếu chưa thống nhất;
- migration/seed phải có cách rollback hoặc reset an toàn.

---

## 20. Anti-patterns phải tránh

- dùng LLM output trực tiếp làm điểm cuối;
- parse JSON bằng regex không có validation;
- hard-code danh sách Role/Skill trong frontend;
- lưu file CV vào thư mục public;
- dùng user ID từ request mà không đối chiếu token;
- tải toàn bộ history rồi cắt/ẩn giới hạn Free ở frontend;
- cho client tự khai báo loại gói để lấy thêm lịch sử;
- hiển thị Matching/Gap/Roadmap trong lịch sử khi pipeline MVP chưa tạo dữ liệu đó;
- xóa history đồng thời xóa CV gốc mà không có yêu cầu riêng;
- chỉ ẩn nội dung Premium bằng CSS;
- ghi raw prompt/response chứa toàn bộ CV vào log;
- gọi OCR mặc định cho mọi file;
- đưa model name cố định vào nhiều nơi;
- thay đổi scoring config mà không version;
- xóa cứng Role có lịch sử;
- trả lỗi kỹ thuật khó hiểu cho người dùng;
- tự thêm tính năng ngoài MVP để “hoàn thiện hơn”.

---

## 21. Mẫu báo cáo sau khi hoàn thành task

```markdown
## Đã thực hiện
- ...

## Use case liên quan
- UC-...

## File đã thay đổi
- `path/to/file`: ...

## Quyết định kỹ thuật
- ...

## Kiểm thử
- `command`: kết quả

## NFR/Security
- ...

## Chưa hoàn thiện hoặc rủi ro
- ...

## Cập nhật plan.md
- Milestone ...: ...
```

---

## 22. Checklist trước khi trả lời hoặc sửa code

- [ ] Tôi đã đọc `plan.md` và `skills.md`.
- [ ] Tôi biết UC và actor liên quan.
- [ ] Tôi không mở rộng ngoài MVP.
- [ ] Tôi không thay đổi stack.
- [ ] Tôi không để secret trong code.
- [ ] Tôi đã cân nhắc privacy của CV.
- [ ] Tôi đã thiết kế backend RBAC.
- [ ] Với history, ownership và Free/Premium entitlement được kiểm tra server-side.
- [ ] Tôi chỉ hiển thị field kết quả thực sự tồn tại trong MVP.
- [ ] Điểm số có thể giải thích và version hóa.
- [ ] AI output được validate.
- [ ] Tôi đã có test cho luồng lỗi.
- [ ] Tôi đã cập nhật tiến độ/tài liệu khi cần.

