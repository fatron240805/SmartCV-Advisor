# Agents.md — Dự án “SmartCV Advisor” (MVP UI Prototype cho Figma Make)

---

## 1. Tổng quan dự án

**SmartCV Advisor** là nền tảng web SaaS ứng dụng AI, hỗ trợ sinh viên, người mới tốt nghiệp, Fresher/Junior và người đang gặp khó khăn khi tìm việc **đánh giá chất lượng CV trước khi ứng tuyển**.

Slogan của dự án: **“Elevate Your Career — Beyond Just a Resume.”**

Trong tầm nhìn dài hạn, sản phẩm có thể phát triển thành một trợ lý nghề nghiệp toàn diện gồm phân tích CV, so khớp CV với Job Description, xác định khoảng cách kỹ năng, đề xuất lộ trình học tập và hỗ trợ chỉnh sửa CV bằng AI.

Tuy nhiên, tài liệu này **chỉ định hướng thiết kế prototype cho MVP đầu tiên**. Figma Make phải ưu tiên luồng phân tích CV cơ bản và không tự mở rộng sang các chức năng nâng cao chưa thuộc MVP.

### Vấn đề MVP cần giải quyết

Người dùng mục tiêu thường gặp các vấn đề sau:

- Không biết CV hiện tại tốt hay chưa.
- Không biết CV mắc lỗi ở bố cục, nội dung, từ khóa, văn phong hoặc khả năng đọc bởi ATS.
- Không biết lỗi nào cần sửa trước.
- Không có một quy trình đơn giản để tải CV, nhận điểm và xem hướng cải thiện.

### Giá trị cốt lõi của MVP

MVP phải giúp người dùng trả lời ba câu hỏi:

1. **CV của tôi đang đạt bao nhiêu điểm?**
2. **CV đang mắc những lỗi phổ biến nào?**
3. **Tôi nên cải thiện CV theo hướng nào trước?**

---

## 2. Phạm vi MVP bắt buộc

### 2.1 Chức năng cốt lõi phải có

Phiên bản đầu tiên tập trung vào đúng các khả năng sau:

1. **Tải CV** dưới định dạng PDF, DOC hoặc DOCX.
2. **Xin sự đồng ý xử lý dữ liệu cá nhân** trước khi tải CV.
3. **Chọn ngành nghề/vị trí mục tiêu** từ danh mục giới hạn trong MVP.
4. **Trích xuất nội dung CV** và mô phỏng tiến trình hệ thống đọc tài liệu.
5. **Chấm điểm CV cơ bản** theo thang điểm 0–100.
6. **Hiển thị điểm tổng quan và điểm thành phần**, gồm:
   - Bố cục.
   - Nội dung.
   - Từ khóa.
   - Văn phong.
   - Độ tương thích ATS.
7. **Phát hiện và liệt kê lỗi phổ biến**, ví dụ:
   - Thiếu thông tin liên hệ.
   - Font chữ hoặc định dạng không nhất quán.
   - Mô tả kinh nghiệm quá chung chung.
   - Thiếu số liệu hoặc kết quả cụ thể.
   - Sai hoặc không thống nhất định dạng ngày tháng.
   - Thiếu từ khóa nền tảng của vị trí mục tiêu.
   - Có thông tin thời gian mâu thuẫn trong CV.
8. **Đưa ra gợi ý cải thiện tổng quan** theo từng nhóm lỗi.
9. **Quản lý tài khoản cơ bản**: đăng ký, đăng nhập, đăng xuất, xem/cập nhật hồ sơ.
10. **Xem gói dịch vụ** và trạng thái gói hiện tại.
11. **Các màn hình quản trị tối thiểu** để quản lý vị trí IT, trọng số kỹ năng và người dùng.

### 2.2 Giới hạn dữ liệu ngành nghề trong MVP

Để MVP có phạm vi kiểm soát được, prototype ưu tiên một nhóm nhỏ vị trí IT cốt lõi, ví dụ:

- Frontend Developer.
- Backend Developer.
- Full-stack Developer.
- Data Analyst.
- UI/UX Designer.
- QA/QC Engineer.

Danh sách này là dữ liệu mẫu cho prototype, không phải cam kết rằng MVP phải hỗ trợ toàn bộ ngành nghề.

### 2.3 Ngoài phạm vi MVP

**Không được thiết kế các chức năng sau như chức năng đã hoạt động hoàn chỉnh:**

- So khớp CV với Job Description.
- Matching Score giữa CV và JD.
- Keyword Gap theo một JD cụ thể.
- Skill Gap chuyên sâu.
- Lộ trình up-skilling 1 tuần/1 tháng/3 tháng.
- AI Assistant dạng chat để viết lại CV.
- Trình tạo CV hoặc chỉnh sửa CV trực tiếp trên canvas.
- Tải xuống CV đã chỉnh sửa.
- Tự động nộp CV vào doanh nghiệp.
- Quản lý tuyển dụng cho doanh nghiệp.
- Thanh toán thật hoặc tích hợp cổng thanh toán VNPay thật. Prototype chỉ mô phỏng luồng thanh toán VNPay bằng dữ liệu/local state theo UC 026.
- B2B cho trường đại học/trung tâm đào tạo.

Các chức năng tương lai có thể xuất hiện trên trang gói dịch vụ dưới nhãn **“Sắp ra mắt”**, nhưng không được tạo luồng sử dụng giả như đã hoàn thiện trong MVP.

### 2.4 Cách xử lý nội dung Premium trong prototype

Đặc tả Use Case có phân biệt Registered User và Premium User. Để không vượt phạm vi MVP:

- **Registered User** xem điểm đầy đủ, lỗi cơ bản và checklist gợi ý tổng quan.
- Giao diện có thể hiển thị một số khối **“Gợi ý chi tiết — Premium”** ở trạng thái khóa để kiểm thử khả năng chuyển đổi.
- Các câu mẫu viết lại chi tiết theo STAR chỉ được dùng như **dữ liệu mock tĩnh** trong prototype Premium, không ngụ ý rằng AI Assistant hoặc trình chỉnh sửa CV đã thuộc MVP.
- Gói Premium được đặt tên hiển thị là **“Premium — Job Search Pass”** để phù hợp với mô hình sử dụng theo chiến dịch tìm việc.

---

## 3. Người dùng và quyền truy cập

### 3.1 Guest

Có thể:

- Xem Landing Page.
- Xem giới thiệu sản phẩm.
- Xem gói dịch vụ.
- Đăng ký.
- Đăng nhập.

Không thể:

- Tải CV.
- Phân tích CV.
- Xem kết quả cá nhân.

### 3.2 Registered User — Free

Có thể:

- Quản lý hồ sơ cá nhân.
- Tải CV và đồng ý chính sách xử lý dữ liệu.
- Chọn vị trí mục tiêu trong danh mục MVP.
- Phân tích CV.
- Xem điểm tổng quan và điểm thành phần.
- Xem lỗi phổ biến.
- Xem gợi ý cải thiện tổng quan.
- Xem lịch sử phân tích tối thiểu.
- Xem gói dịch vụ.

Giới hạn gợi ý cho prototype:

- Hiển thị trạng thái **“Còn 2/3 lượt phân tích trong tháng”**.
- Không cần hiện thực cơ chế tính lượt thật; dùng mock data.

### 3.3 Premium User

Trong prototype, Premium User có thể:

- Xem toàn bộ chức năng của Registered User.
- Xem khối gợi ý chi tiết mở khóa.
- Sao chép câu mẫu bằng nút **“Sao chép”**.
- Xem ngày hết hạn gói và nút **“Gia hạn”**.

Không tự thêm các chức năng tương lai như Matching Score, Roadmap hoặc AI Chat vào luồng chính.

### 3.4 Admin

Có thể:

- Quản lý danh sách vị trí IT.
- Quản lý kỹ năng, điểm và trọng số theo vị trí.
- Quản lý người dùng.

Admin sử dụng giao diện quản trị riêng, không dùng chung dashboard người tìm việc.

---

## 4. Tech Stack và giới hạn triển khai prototype

| Thành phần | Công nghệ/Quy ước |
| --- | --- |
| Frontend | **React + Tailwind CSS** |
| Backend định hướng | **Python + FastAPI** |
| Database, Auth, Storage | **Supabase** |
| Xử lý CV | Pipeline trích xuất nội dung và chấm điểm AI; trong prototype Figma dùng dữ liệu mock |
| Triển khai định hướng | Vercel cho frontend, Render cho backend |
| Prototype hiện tại | Tập trung vào UI, interaction và trạng thái; không cần kết nối API thật |

### Quy tắc kỹ thuật cho Figma Make

- Nếu sinh mã giao diện, dùng React và Tailwind CSS; không tự đổi sang Vue, Angular hoặc framework khác.
- Dữ liệu phải được tách thành mock objects để dễ thay bằng API sau này.
- Không hard-code API key hoặc thông tin xác thực.
- Không cần tích hợp OpenAI, Anthropic, Hugging Face hoặc Supabase thật trong bản prototype UI.
- Các thao tác upload, phân tích, lưu hồ sơ, nâng cấp gói và quản trị được mô phỏng bằng local state/mock data.
- Component phải có cấu trúc tái sử dụng và sẵn sàng nối với FastAPI/Supabase sau này.

---

## 5. Kiến trúc thông tin và điều hướng

### 5.1 Điều hướng dành cho Guest

Thanh điều hướng trên cùng:

- Logo **SmartCV Advisor**.
- Trang chủ.
- Cách hoạt động.
- Gói dịch vụ.
- Đăng nhập.
- Nút chính: **“Phân tích CV miễn phí”**.

Khi Guest chọn “Phân tích CV miễn phí”, hệ thống chuyển đến Đăng ký/Đăng nhập.

### 5.2 Điều hướng dành cho Registered/Premium User

Sidebar desktop hoặc bottom navigation trên mobile:

- Tổng quan.
- Phân tích CV.
- Lịch sử phân tích.
- Gói dịch vụ.
- Hồ sơ cá nhân.

Menu tài khoản:

- Thông tin cá nhân.
- Gói hiện tại.
- Đăng xuất.

### 5.3 Điều hướng dành cho Admin

Sidebar cố định:

- Tổng quan quản trị.
- Vị trí IT.
- Kỹ năng & Điểm số.
- Người dùng.
- Đăng xuất.

Không thêm các module quản trị ngoài ba nhóm Use Case đã đặc tả.

---

## 6. Luồng trải nghiệm chính của MVP

### Luồng A — Guest bắt đầu sử dụng

1. Guest mở Landing Page.
2. Guest chọn **“Phân tích CV miễn phí”**.
3. Hệ thống chuyển đến màn hình Đăng ký hoặc Đăng nhập.
4. Nếu chọn đăng ký, Guest nhập họ tên, email, mật khẩu và xác nhận mật khẩu.
5. Guest đọc và đồng ý với Điều khoản sử dụng cùng Chính sách quyền riêng tư.
6. Hệ thống tạo tài khoản Registered User và gửi email xác thực.
7. Hệ thống hiển thị thông báo yêu cầu kiểm tra email, kèm tùy chọn **“Gửi lại email xác thực”**.
8. Người dùng mở liên kết xác thực; hệ thống kích hoạt tài khoản và chuyển đến trang Đăng nhập.
9. Người dùng đăng nhập thành công.
10. Hệ thống xác định vai trò và chuyển đến Dashboard tương ứng.

### Luồng B — Phân tích CV lần đầu

1. Người dùng chọn **“Phân tích CV mới”**.
2. Hệ thống hiển thị khu vực chọn tệp và kéo thả CV.
3. Người dùng chọn tệp PDF/DOC/DOCX.
4. Hệ thống kiểm tra định dạng, dung lượng, tình trạng tệp và khả năng đọc nội dung; sau đó hiển thị tên tệp, định dạng, dung lượng và trạng thái kiểm tra.
5. Hệ thống hiển thị thông báo về dữ liệu cá nhân, liên kết đến Chính sách quyền riêng tư/Điều khoản xử lý dữ liệu và checkbox đồng ý.
6. Chỉ khi tệp hợp lệ và checkbox được chọn, nút **“Xác nhận và tải CV lên”** mới hoạt động.
7. Hệ thống hiển thị tiến trình tải lên; người dùng có thể hủy hoặc thay tệp trước khi hoàn tất.
8. Sau khi tải thành công, người dùng chọn vị trí mục tiêu.
9. Người dùng chọn **“Bắt đầu phân tích”**.
10. Hệ thống hiển thị màn hình tiến trình, tối đa mô phỏng 30 giây.
11. Hệ thống tự động chuyển đến trang kết quả.
12. Người dùng xem điểm, lỗi và gợi ý cải thiện.

### Luồng C — Xem lại kết quả

1. Người dùng mở **“Lịch sử phân tích”**.
2. Hệ thống hiển thị danh sách bản phân tích tối thiểu.
3. Người dùng chọn một bản ghi.
4. Hệ thống mở lại trang kết quả tương ứng.

### Luồng D — Mở nội dung Premium và thanh toán mô phỏng

1. Registered User chọn một khối gợi ý chi tiết có biểu tượng khóa.
2. Hệ thống mở modal giải thích quyền lợi Premium.
3. Người dùng có thể chọn **“Xem gói Premium”** hoặc **“Để sau”**.
4. Nếu chọn xem gói, hệ thống chuyển đến trang Gói dịch vụ.
5. Người dùng chọn gói Premium và nhấn **“Nâng cấp Premium”**.
6. Hệ thống chuyển đến màn hình thanh toán **VNPay mô phỏng**.
7. Người dùng xác nhận thanh toán; hệ thống mô phỏng kết quả thành công hoặc thất bại.
8. Khi thành công, local state/mock data cập nhật trạng thái gói Premium và ngày hết hạn.
9. Không tích hợp cổng VNPay thật hoặc xử lý tiền thật trong prototype.

### Luồng E — Xóa dữ liệu cá nhân

1. Người dùng mở Hồ sơ cá nhân.
2. Người dùng chọn **“Quản lý dữ liệu CV”**.
3. Hệ thống hiển thị các bản CV đã tải lên ở mức tối thiểu.
4. Người dùng chọn **“Xóa dữ liệu CV”**.
5. Hệ thống mở modal cảnh báo hậu quả.
6. Người dùng xác nhận.
7. Hệ thống hiển thị thông báo xóa thành công.

### Luồng F — Quên và đặt lại mật khẩu

1. Người dùng chọn **“Quên mật khẩu?”** tại màn hình Đăng nhập.
2. Hệ thống yêu cầu nhập email tài khoản.
3. Người dùng gửi yêu cầu đặt lại mật khẩu.
4. Hệ thống mô phỏng việc gửi liên kết đặt lại mật khẩu qua email.
5. Người dùng mở liên kết và nhập mật khẩu mới cùng xác nhận mật khẩu.
6. Hệ thống kiểm tra dữ liệu, cập nhật mật khẩu và chuyển về trang Đăng nhập.
7. Hệ thống hiển thị thông báo đặt lại mật khẩu thành công.

---

## 7. Danh sách màn hình cần tạo

## Nhóm 1 — Public và xác thực

### Screen P01 — Landing Page

**Mục tiêu:** Giải thích sản phẩm và đưa người dùng vào luồng phân tích CV.

**Bố cục:**

1. Header.
2. Hero section hai cột:
   - Trái: tiêu đề, mô tả, CTA.
   - Phải: mockup báo cáo điểm CV.
3. “SmartCV Advisor giúp bạn làm gì?” gồm 3 bước:
   - Tải CV.
   - Nhận điểm và phát hiện lỗi.
   - Xem hướng cải thiện.
4. Khối minh họa 5 tiêu chí đánh giá.
5. Khối nhấn mạnh quyền riêng tư.
6. Preview gói Free/Premium.
7. Footer.

**Nội dung gợi ý:**

- H1: **“Biết CV của bạn cần sửa gì trước khi ứng tuyển.”**
- Mô tả: “Tải CV, nhận điểm đánh giá theo vị trí mục tiêu và xem các lỗi cần ưu tiên cải thiện.”
- CTA chính: **“Phân tích CV miễn phí”**.
- CTA phụ: **“Xem cách hoạt động”**.

**Không được:**

- Quảng bá Matching Score, Skill Gap, Roadmap hoặc AI Chat như tính năng đang hoạt động.
- Dùng hình ảnh robot hoặc hiệu ứng AI viễn tưởng quá mức.

### Screen P02 — Đăng ký

**Use Case:** UC 008.

**Thành phần:**

- Logo.
- Tiêu đề: **“Tạo tài khoản SmartCV Advisor”**.
- Họ và tên.
- Email.
- Mật khẩu.
- Xác nhận mật khẩu.
- Hiển thị/ẩn mật khẩu.
- Checklist yêu cầu mật khẩu tối thiểu 8 ký tự, có chữ và số.
- Checkbox bắt buộc: **“Tôi đồng ý với Điều khoản sử dụng và Chính sách quyền riêng tư.”**
- Link mở Điều khoản sử dụng và Chính sách quyền riêng tư.
- Nút **“Đăng ký tài khoản”**, bị vô hiệu hóa khi dữ liệu chưa hợp lệ hoặc chưa đồng ý điều khoản.
- Link **“Đã có tài khoản? Đăng nhập”**.

**Trạng thái:** mặc định, đang nhập, thiếu trường bắt buộc, email sai định dạng, email trùng, mật khẩu yếu, mật khẩu không khớp, chưa đồng ý điều khoản, đang xử lý và đăng ký thành công.

### Screen P02A — Xác thực email

**Use Case:** UC 008, sau khi đăng ký thành công.

**Thành phần:**

- Icon email và tiêu đề **“Kiểm tra email của bạn”**.
- Mô tả: “Chúng tôi đã gửi liên kết xác thực đến `m***@example.com`.”
- Nút **“Gửi lại email xác thực”**.
- Trạng thái đếm thời gian trước khi cho gửi lại để tránh nhấn liên tục.
- Link **“Quay lại đăng nhập”**.
- Trạng thái xác thực thành công: **“Tài khoản đã được kích hoạt”** và CTA **“Đăng nhập”**.
- Trạng thái lỗi khi liên kết hết hạn hoặc không hợp lệ, kèm CTA gửi lại email.

### Screen P03 — Đăng nhập

**Use Case:** UC 009.

**Thành phần:**

- Email.
- Mật khẩu.
- Checkbox **“Ghi nhớ đăng nhập”**.
- Link **“Quên mật khẩu?”**.
- Nút **“Đăng nhập”**.
- Link đến Đăng ký.

**Sau khi đăng nhập thành công:**

- Hệ thống xác định vai trò Registered User, Premium User hoặc Admin.
- Registered/Premium User được chuyển đến Dashboard người dùng.
- Admin được chuyển đến Tổng quan quản trị.
- Hiển thị toast **“Đăng nhập thành công.”**

**Trạng thái lỗi:**

- “Thông tin đăng nhập không chính xác.”
- “Tài khoản của bạn chưa được xác thực. Vui lòng kiểm tra email.” kèm nút “Gửi lại email xác thực”.
- “Tài khoản của bạn đã bị tạm khóa.”
- Cảnh báo sau nhiều lần nhập sai.

### Screen P03A — Quên mật khẩu

**Use Case:** UC 009, Alternative Flow A3.1.

- Tiêu đề: **“Đặt lại mật khẩu”**.
- Ô nhập email.
- Nút **“Gửi liên kết đặt lại mật khẩu”**.
- Trạng thái đang gửi, gửi thành công và email sai định dạng.
- Thông báo thành công: **“Liên kết đặt lại mật khẩu đã được gửi. Vui lòng kiểm tra email.”**
- Link quay lại Đăng nhập.

### Screen P03B — Tạo mật khẩu mới

**Use Case:** UC 009, sau khi người dùng mở liên kết đặt lại mật khẩu.

- Mật khẩu mới.
- Xác nhận mật khẩu mới.
- Checklist độ mạnh mật khẩu.
- Nút **“Cập nhật mật khẩu”**.
- Trạng thái liên kết hợp lệ, liên kết hết hạn, mật khẩu không khớp và cập nhật thành công.
- Sau khi thành công, chuyển về trang Đăng nhập.

### Modal P04 — Xác nhận đăng xuất

**Use Case:** UC 010.

- Tiêu đề: **“Bạn có chắc chắn muốn đăng xuất không?”**
- Mô tả ngắn về việc kết thúc phiên làm việc hiện tại.
- Nút phụ: **“Hủy”** — đóng modal và giữ nguyên phiên đăng nhập.
- Nút chính: **“Xác nhận đăng xuất”** — xóa dữ liệu xác thực trên thiết bị, chuyển về trang chủ hoặc Đăng nhập và hiển thị toast **“Đăng xuất thành công.”**

### Modal/State P05 — Phiên đăng nhập hết hạn

**Use Case:** UC 010, Alternative Flow A7.

- Hệ thống tự động kết thúc phiên đăng nhập.
- Thông báo: **“Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.”**
- CTA duy nhất: **“Đăng nhập lại”**.
- Không giữ nội dung nhạy cảm của phiên cũ trên màn hình.

---

## Nhóm 2 — Dashboard và hồ sơ người dùng

### Screen U01 — Dashboard người dùng

**Mục tiêu:** Cho người dùng biết trạng thái tài khoản và bắt đầu phân tích mới nhanh nhất.

**Bố cục:**

- Header chào người dùng.
- Card CTA lớn **“Phân tích CV mới”**.
- Card số lượt còn lại: “2/3 lượt trong tháng”.
- Card kết quả gần nhất:
  - Tên tệp.
  - Vị trí mục tiêu.
  - Điểm tổng.
  - Ngày phân tích.
  - Nút “Xem kết quả”.
- Danh sách 3 bản phân tích gần đây.
- Banner nhỏ về Premium, không gây cản trở luồng chính.

**Empty state:**

- “Bạn chưa phân tích CV nào.”
- CTA: “Tải CV đầu tiên”.

### Screen U02 — Hồ sơ cá nhân

**Use Case:** UC 011.

**Tab 1 — Thông tin cá nhân:**

- Avatar.
- Họ và tên.
- Email ở trạng thái readonly hoặc có cảnh báo xác thực khi đổi.
- Ngành nghề quan tâm.
- Vị trí mục tiêu mặc định.
- Trình độ hiện tại.
- Trạng thái xem và trạng thái **“Chỉnh sửa thông tin”**.
- Nút **“Lưu thay đổi”** và nút **“Hủy”**; khi hủy, hệ thống khôi phục dữ liệu đã lưu gần nhất.
- Luồng đổi avatar: chọn ảnh → kiểm tra định dạng/dung lượng → xem trước → xác nhận.
- Khi đổi vị trí mục tiêu, hệ thống lưu Role IT mới để dùng cho các lần đánh giá tiếp theo; không tự mở Roadmap trong MVP.

**Tab 2 — Dữ liệu & quyền riêng tư:**

- Mô tả dữ liệu CV đang lưu.
- Danh sách tệp CV tối thiểu.
- Nút “Xóa dữ liệu CV”.
- Thông báo: “CV của bạn không được dùng để huấn luyện mô hình nếu chưa có sự đồng ý.”

**Trạng thái:** lưu thành công, email trùng, ảnh đại diện sai định dạng, xác nhận xóa dữ liệu.

### Screen U03 — Lịch sử phân tích tối thiểu

**Mục tiêu hỗ trợ:** Cho phép mở lại kết quả theo trigger của UC 015.

**Không phát triển thành hệ thống quản lý tài liệu phức tạp.**

**Danh sách gồm:**

- Tên file.
- Vị trí mục tiêu.
- Điểm tổng.
- Xếp loại.
- Ngày phân tích.
- Nút “Xem kết quả”.

**Bộ lọc tối thiểu:** tìm theo tên file, lọc theo vị trí mục tiêu.

---

## Nhóm 3 — Luồng phân tích CV cốt lõi

### Screen A01 — Tải CV

**Use Case:** UC 012.

**Bố cục:**

- Stepper: `1. Tải CV` → `2. Chọn vị trí` → `3. Phân tích` → `4. Kết quả`.
- Tiêu đề: **“Tải CV của bạn lên”**.
- Vùng drag-and-drop lớn.
- Icon file.
- Dòng hỗ trợ: “PDF, DOC hoặc DOCX — tối đa 5 MB”.
- Nút **“Chọn tệp CV”**.

**Sau khi chọn tệp:**

- Hệ thống kiểm tra định dạng, dung lượng, khả năng đọc và tình trạng tệp.
- Card file hiển thị:
  - Tên tệp.
  - Định dạng.
  - Dung lượng.
  - Trạng thái kiểm tra.
  - Nút **“Chọn tệp khác”** và xóa tệp.

**Khối đồng ý xử lý dữ liệu:**

- Thông báo rõ: **“CV có thể chứa thông tin cá nhân như họ tên, email, số điện thoại, học vấn và kinh nghiệm làm việc. Hệ thống cần xử lý các dữ liệu này để thực hiện phân tích và đưa ra đề xuất cải thiện CV. Vui lòng xác nhận đồng ý trước khi tiếp tục.”**
- Checkbox bắt buộc: **“Tôi đồng ý cho phép hệ thống xử lý dữ liệu trong CV nhằm phục vụ việc phân tích và đưa ra đề xuất.”**
- Link **“Chính sách quyền riêng tư”**.
- Link **“Điều khoản xử lý dữ liệu”**.

**CTA:**

- **“Xác nhận và tải CV lên”**.
- Disable khi chưa có file hợp lệ hoặc chưa đồng ý.
- Khi chưa đồng ý, hiển thị hỗ trợ: **“Bạn cần đồng ý với chính sách xử lý dữ liệu CV để tiếp tục.”**

**Trong khi tải lên:**

- Progress bar theo phần trăm.
- Nút **“Hủy tải lên”**; khi hủy, hệ thống dừng tiến trình, xóa dữ liệu tạm và quay lại màn hình chọn CV.
- Sau khi thành công, hiển thị toast **“Tải CV lên thành công.”** và chuyển đến Screen A02.

**Trạng thái lỗi:**

- Sai định dạng.
- File lớn hơn 5 MB.
- Upload thất bại.
- File có thể bị hỏng hoặc không thể đọc.
- Chưa đồng ý xử lý dữ liệu.
- Đã hủy tải lên.

### Screen A02 — Chọn vị trí mục tiêu

**Use Case:** UC 013.

**Bố cục:**

- Stepper đang ở bước 2.
- Tiêu đề: **“Bạn muốn đánh giá CV cho vị trí nào?”**
- Ô tìm kiếm vị trí.
- Danh sách card vị trí IT.
- Một card được chọn phải có viền primary và check icon.
- Panel bên phải hoặc phía dưới hiển thị mô tả ngắn vị trí đã chọn.

**CTA:**

- “Quay lại”.
- “Xác nhận vị trí”.

**Trạng thái:** loading danh mục, không tìm thấy, lỗi tải danh mục.

**Không được:**

- Cho nhập Job Description.
- Hứa hẹn Matching Score.

### Screen A03 — Xác nhận trước khi phân tích

**Mục tiêu:** Giảm lỗi thao tác trước khi dùng lượt phân tích.

**Hiển thị:**

- Tên file.
- Dung lượng.
- Vị trí mục tiêu.
- Số lượt còn lại.
- Nhắc lại loại kết quả sẽ nhận: điểm, lỗi phổ biến, gợi ý tổng quan.

**CTA chính:** **“Bắt đầu phân tích”**.

### Screen A04 — Đang phân tích CV

**Use Case:** UC 014.

**Bố cục:**

- Stepper ở bước 3.
- Tiêu đề: **“Đang phân tích CV của bạn”**.
- Progress bar hoặc progress ring.
- Danh sách giai đoạn có check/progress:
  1. Đang đọc nội dung CV.
  2. Đang nhận diện các phần trong CV.
  3. Đang đánh giá theo vị trí mục tiêu.
  4. Đang tổng hợp điểm và lỗi.
- Dòng thời gian: “Quá trình này thường mất dưới 30 giây.”
- Không cho người dùng tải tệp khác giữa tiến trình.

**State mô phỏng:**

- 0–20%: Đọc tệp.
- 20–45%: Trích xuất nội dung.
- 45–75%: Chấm điểm tiêu chí.
- 75–100%: Tổng hợp nhận xét.

**Trạng thái lỗi:**

- “Tệp tin lỗi hoặc không thể đọc nội dung.”
- “Hệ thống đang bận, vui lòng thử lại sau.”
- CTA: “Thử lại” và “Chọn tệp khác”.

### Modal A05 — Cảnh báo thông tin mâu thuẫn

**Thuộc UC 014.**

Dùng khi hệ thống phát hiện mốc thời gian bất hợp lý, ví dụ số năm kinh nghiệm lớn hơn khoảng thời gian học/làm được khai báo.

**Nội dung:**

- Tiêu đề: **“Có thông tin cần bạn kiểm tra lại”**.
- Mô tả trung lập, không kết luận người dùng khai gian.
- Ví dụ: “CV ghi 5 năm kinh nghiệm SQL nhưng mốc thời gian liên quan hiện chỉ thể hiện khoảng 3 năm.”
- Nút “Tiếp tục xem kết quả”.
- Nút “Tải CV khác”.

**Giọng điệu:** hỗ trợ, không phán xét.

### Screen R01 — Tổng quan kết quả

**Use Case:** UC 015.

**Bố cục desktop:**

- Header kết quả gồm tên file, vị trí mục tiêu, ngày phân tích.
- Cột trái: CV score card lớn.
- Cột phải: tóm tắt điểm mạnh, vấn đề cần ưu tiên.
- Phía dưới: điểm 5 tiêu chí và danh sách lỗi.

**Score card:**

- Donut chart lớn, ví dụ `72/100`.
- Xếp loại: “Khá”.
- Thông điệp: “CV đã có nền tảng tốt nhưng cần làm rõ kết quả và chuẩn hóa định dạng.”

**Điểm thành phần:**

- Bố cục: 82.
- Nội dung: 68.
- Từ khóa: 70.
- Văn phong: 74.
- ATS: 66.

Dùng thanh điểm ngang hoặc card nhỏ. Không bắt buộc dùng Radar chart nếu làm giảm khả năng đọc.

**Tabs:**

- Tổng quan.
- Bố cục.
- Nội dung.
- Từ khóa.
- Văn phong.
- ATS.

**CTA:**

- “Xem gợi ý cải thiện”.
- “Phân tích CV khác”.

### Screen R02 — Chi tiết lỗi theo tiêu chí

**Use Case:** UC 015.

Mỗi issue card gồm:

- Mức độ: Cần ưu tiên / Nên cải thiện / Đã làm tốt.
- Tên lỗi.
- Mô tả ngắn.
- Vì sao lỗi này ảnh hưởng CV.
- Nút “Xem cách cải thiện”.

**Mức độ dùng màu:**

- Đỏ: Cần ưu tiên.
- Vàng/cam: Nên cải thiện.
- Xanh lá: Đã làm tốt.

Không chỉ dùng màu; luôn có nhãn chữ và icon.

### Screen R03 — Gợi ý cải thiện tổng quan

**Use Case:** UC 016.

**Bố cục:**

- Header: “Gợi ý cải thiện CV”.
- Bộ lọc theo tiêu chí.
- Danh sách checklist ưu tiên.

Mỗi suggestion card gồm:

- Vấn đề liên quan.
- Hành động đề xuất.
- Mức ưu tiên.
- Ví dụ ngắn ở mức tổng quan.
- Checkbox “Đã xem” hoặc “Đã xử lý” chỉ dùng trong prototype, không cần lưu thật.

**Ví dụ:**

- “Bổ sung kết quả định lượng cho ít nhất hai dự án quan trọng.”
- “Thống nhất định dạng tháng/năm trong phần Kinh nghiệm và Học vấn.”
- “Đưa kỹ năng ReactJS, REST API và Git vào phần Kỹ năng nếu đúng với kinh nghiệm thực tế.”
- “Rút ngắn phần Mục tiêu nghề nghiệp còn 2–3 câu.”

**Khối Premium bị khóa:**

- Tiêu đề: “Câu mẫu viết lại theo STAR”.
- Hiển thị preview mờ hoặc skeleton.
- Icon khóa.
- Nút “Mở khóa với Premium”.

### Screen R04 — Gợi ý Premium mở khóa

**Use Case:** UC 016, trạng thái Premium User.

**Dùng mock data tĩnh.**

Mỗi câu mẫu gồm:

- Nội dung hiện tại.
- Gợi ý viết lại.
- Lý do gợi ý.
- Nút **“Sao chép”**.
- Nhãn nhắc: “Chỉ sử dụng thông tin đúng với kinh nghiệm thực tế của bạn.”

Không tạo trình soạn thảo CV hoặc AI chat.

---

## Nhóm 4 — Gói dịch vụ

### Screen S01 — Danh sách gói dịch vụ

**Use Case:** UC 026.

**Bố cục:**

- Header: “Chọn gói phù hợp với giai đoạn tìm việc của bạn”.
- Toggle thời hạn 30 ngày / 90 ngày cho Premium — Job Search Pass.
- Hai card chính:
  - Free.
  - Premium — Job Search Pass.

**Gói Free:**

- 3 lượt phân tích/tháng.
- Xem điểm tổng quan và điểm thành phần.
- Xem lỗi phổ biến.
- Gợi ý cải thiện tổng quan.

**Gói Premium — Job Search Pass:**

- Nhiều lượt phân tích hơn hoặc không giới hạn trong thời hạn gói — chỉ hiển thị như mock.
- Gợi ý chi tiết.
- Câu mẫu viết lại.
- Sao chép nhanh.

**Tính năng tương lai:**

Các mục sau phải có badge **“Sắp ra mắt”** thay vì dấu tick đang hoạt động:

- Matching Score.
- Keyword Gap theo JD.
- Skill Gap.
- Roadmap.
- AI Assistant.
- Download CV đã chỉnh sửa.

**Trạng thái theo actor:**

- Guest: nút “Đăng ký để bắt đầu”.
- Registered User: nhãn “Gói hiện tại” trên Free và nút “Nâng cấp Premium”.
- Premium User: nhãn “Đang hoạt động”, ngày hết hạn và nút “Gia hạn”.

**CTA nâng cấp chuyển đến Screen S02 — VNPay mô phỏng.** Không tích hợp VNPay thật, không xử lý tiền thật và không lưu thông tin thanh toán nhạy cảm.

### Screen S02 — Thanh toán VNPay mô phỏng

**Use Case:** UC 026, bước chuyển tiếp sau khi Registered User chọn nâng cấp Premium.

**Bố cục:**

- Nhãn rõ **“MÔ PHỎNG — Không phát sinh giao dịch thật”**.
- Logo/khung nhận diện VNPay ở mức minh họa, không giả lập trang ngân hàng thật.
- Tóm tắt đơn hàng:
  - Tên gói.
  - Thời hạn 30 ngày hoặc 90 ngày.
  - Giá mock.
  - Mã đơn hàng mock.
- Khu vực chọn phương thức thanh toán mô phỏng.
- Nút **“Xác nhận thanh toán mô phỏng”**.
- Nút **“Hủy và quay lại gói dịch vụ”**.

**Trạng thái:**

- Đang xử lý.
- Thành công: hiển thị mã giao dịch mock, ngày kích hoạt, ngày hết hạn và CTA **“Về Dashboard”**.
- Thất bại: hiển thị lý do mô phỏng và CTA **“Thử lại”** hoặc **“Quay lại gói dịch vụ”**.
- Người dùng đóng/hủy giữa chừng: không thay đổi trạng thái gói.

---

## Nhóm 5 — Giao diện quản trị

### Screen AD01 — Quản lý vị trí IT

**Use Case:** UC 001.

**Bố cục:**

- Header trang.
- Nút “Thêm vị trí IT”.
- Search.
- Bộ lọc trạng thái.
- Table gồm:
  - Tên vị trí.
  - Mô tả.
  - Trạng thái.
  - Ngày tạo.
  - Cập nhật gần nhất.
  - Thao tác.

**Thao tác:**

- Xem chi tiết.
- Chỉnh sửa.
- Ẩn/Ngưng hoạt động.

**Tìm kiếm và lọc:**

- Tìm theo tên Role IT.
- Lọc theo trạng thái.
- Khi không có kết quả, hiển thị **“Không tìm thấy vị trí IT phù hợp.”**

**Modal/Form thêm-sửa:**

- Tên vị trí.
- Mô tả tổng quan.
- Trạng thái.
- Nút **“Lưu thay đổi”** và **“Hủy”**.
- Khi lưu chỉnh sửa thành công, hiển thị toast **“Cập nhật vị trí IT thành công.”**
- Khi hủy, đóng form, không lưu dữ liệu vừa nhập và quay lại danh sách.

**Ngưng hoạt động:**

- Mở hộp thoại xác nhận trước khi thay đổi trạng thái.
- Sau khi xác nhận, chuyển trạng thái sang **“Ngưng hoạt động”** nhưng giữ nguyên dữ liệu đánh giá CV trước đây.
- Hiển thị toast **“Đã cập nhật trạng thái vị trí IT.”**

**Rule UI:** Nếu vị trí đã được dùng trong lịch sử phân tích, không hiển thị “Xóa vĩnh viễn”; chỉ cho “Ngưng hoạt động”.

### Screen AD02 — Quản lý kỹ năng & điểm số

**Use Case:** UC 002.

**Bố cục:**

- Dropdown chọn Role IT.
- Data grid chỉnh sửa nhanh.
- Cột:
  - Tên kỹ năng.
  - Nhóm kỹ năng.
  - Mức điểm yêu cầu.
  - Trọng số.
  - Mức độ quan trọng.
  - Trạng thái.
  - Thao tác.
- Thanh tổng trọng số, ví dụ `85/100%`.
- Checkbox chọn nhiều dòng.
- Nút **“Thêm kỹ năng”**.
- Nút **“Chỉnh sửa hàng loạt”**, chỉ bật khi có nhiều kỹ năng được chọn.
- Nút **“Lưu thay đổi”** và **“Hủy”**.

**Luồng thêm kỹ năng:**

- Mở modal hiển thị danh sách kỹ năng hiện có.
- Admin chọn kỹ năng, nhập điểm yêu cầu, trọng số và mức độ quan trọng.
- Sau khi lưu thành công, hiển thị **“Thêm kỹ năng thành công.”**

**Luồng chỉnh sửa hàng loạt:**

- Admin chọn nhiều kỹ năng và nhấn **“Chỉnh sửa hàng loạt”**.
- Form cho phép cập nhật điểm số hoặc trọng số cho các dòng đã chọn.
- Hệ thống kiểm tra toàn bộ dữ liệu trước khi áp dụng và hiển thị kết quả cập nhật.
- Nếu Admin chọn **“Hủy”**, hệ thống không lưu thay đổi và khôi phục dữ liệu đã lưu gần nhất.

**Validation:**

- Không cho số âm.
- Không cho ký tự chữ trong ô số.
- Cảnh báo khi tổng trọng số vượt 100%.
- Core Skill phải có threshold > 0.

### Screen AD03 — Quản lý người dùng

**Use Case:** UC 004.

**Bố cục:**

- Search theo họ tên/email.
- Bộ lọc loại tài khoản: Registered User/Premium User.
- Bộ lọc trạng thái: Đang hoạt động/Đã khóa.
- Bộ lọc ngày đăng ký.
- Table tối đa 50 dòng/trang.
- Cột:
  - Họ tên.
  - Email.
  - Loại tài khoản.
  - Trạng thái.
  - Ngày đăng ký.
  - Đăng nhập gần nhất.
  - Thao tác.

**Drawer chi tiết người dùng:**

- Thông tin cơ bản.
- Gói hiện tại.
- Lịch sử gói tối thiểu.
- Số lượt phân tích.
- Trạng thái tài khoản.
- Nút chỉnh sửa.
- Nút khóa/mở khóa.

**Luồng khóa tài khoản:**

- Admin chọn **“Khóa tài khoản”**.
- Modal bắt buộc nhập lý do khóa và yêu cầu xác nhận.
- Sau khi xác nhận, trạng thái chuyển thành **“Đã khóa”** và mọi phiên đăng nhập đang hoạt động của tài khoản bị kết thúc.
- Hiển thị toast **“Khóa tài khoản thành công.”**

**Luồng mở khóa:**

- Với tài khoản đã khóa, hiển thị nút **“Mở khóa”**.
- Admin phải xác nhận trước khi thực hiện.
- Sau khi xác nhận, trạng thái chuyển thành **“Đang hoạt động”**.

**Rule UI:**

- Không cho khóa Admin khác.
- Không cho xóa vĩnh viễn tài khoản Premium còn hiệu lực.
- Không cho xác nhận khóa khi chưa nhập lý do.

---

## 8. Quy tắc thiết kế UI/UX

### 7.1 Định hướng hình ảnh

Phong cách cần thể hiện:

- Chuyên nghiệp.
- Tin cậy.
- Hiện đại nhưng không phô trương AI.
- Phù hợp với sinh viên và người mới đi làm tại Việt Nam.
- Dễ hiểu ngay cả khi người dùng chưa biết ATS là gì.

Tránh:

- Giao diện neon, cyberpunk hoặc quá nhiều gradient.
- Biểu tượng robot, não AI hoặc hiệu ứng khoa học viễn tưởng.
- Dashboard quá nhiều biểu đồ nhỏ.
- Văn bản dài trong một card.
- Giao diện giống hệ thống tuyển dụng doanh nghiệp.

### 7.2 Màu sắc đề xuất

Dùng hệ màu sáng, sạch và có độ tương phản cao.

- Primary 600: `#2563EB`.
- Primary 700: `#1D4ED8`.
- Primary 50: `#EFF6FF`.
- Text primary: `#0F172A`.
- Text secondary: `#475569`.
- Border: `#E2E8F0`.
- Surface: `#FFFFFF`.
- Background: `#F8FAFC`.
- Success: `#16A34A`.
- Warning: `#D97706`.
- Error: `#DC2626`.
- Premium accent: `#7C3AED`, chỉ dùng có kiểm soát cho nội dung Premium.

Không dùng quá nhiều màu cùng lúc. Màu điểm số không được tạo cảm giác “phán xét”; luôn đi cùng mô tả hành động.

### 7.3 Typography

- Font: Inter hoặc font sans-serif tương đương.
- H1: 48–56 px desktop, 34–40 px mobile.
- H2: 32–40 px.
- H3: 22–28 px.
- Body: 16 px.
- Supporting text: tối thiểu 14 px.
- Button: 15–16 px, semibold.

### 7.4 Grid và spacing

- Desktop content max-width: 1200–1280 px.
- 12-column grid.
- Spacing theo bội số 4 hoặc 8.
- Card padding: 20–24 px.
- Border radius: 12–16 px.
- Shadow nhẹ, không tạo card nổi quá mức.

### 7.5 Nút và hành động

- Mỗi màn hình chỉ có một hành động chính rõ ràng.
- Primary button dùng nền xanh.
- Secondary button dùng outline hoặc nền xám nhạt.
- Destructive button dùng đỏ và phải có confirm modal.
- Disabled state phải rõ ràng.
- Loading button có spinner và giữ nguyên chiều rộng.

### 7.6 Biểu đồ và điểm số

- Ưu tiên donut chart cho tổng điểm.
- Dùng horizontal score bars cho điểm thành phần.
- Không chỉ dùng màu để thể hiện kết quả.
- Luôn hiển thị số điểm, tên mức đánh giá và mô tả.
- Không dùng biểu đồ 3D.

---

## 9. Component library cần tạo

### Global

- App header.
- User sidebar.
- Admin sidebar.
- Breadcrumb.
- Stepper 4 bước.
- Page header.
- Toast.
- Modal.
- Confirmation modal.
- Empty state.
- Error state.
- Skeleton loading.

### Form

- Text input.
- Password input.
- Search input.
- Select/dropdown.
- Checkbox.
- Radio/card selection.
- File upload dropzone.
- File preview row.
- Validation message.
- Email verification notice/resend control.
- Password reset form.
- Upload progress row với hành động hủy.

### CV analysis

- Score donut.
- Score progress bar.
- Criteria score card.
- Issue card.
- Suggestion card.
- Premium locked card.
- Copyable rewrite card.
- Analysis progress list.
- Contradiction warning card/modal.

### Admin

- Data table.
- Pagination.
- Filter bar.
- Inline editable grid cell.
- Status badge.
- User detail drawer.
- Role form modal.

---

## 10. Trạng thái giao diện bắt buộc

Mỗi màn hình quan trọng phải có các trạng thái sau khi phù hợp:

- Default.
- Hover.
- Focus.
- Disabled.
- Loading.
- Empty.
- Success.
- Error.
- Locked/Premium.

Đặc biệt:

- Upload phải có drag-over state.
- File hợp lệ và file lỗi phải phân biệt rõ.
- Analysis progress phải có state thành công và thất bại.
- Result page phải có state không tìm thấy bản ghi.
- Pricing phải có state Guest, Free và Premium.
- Registration phải có state chờ xác thực email, gửi lại email và liên kết hết hạn.
- Login phải có state quên mật khẩu và phiên đăng nhập hết hạn.
- Thanh toán VNPay mô phỏng phải có state đang xử lý, thành công, thất bại và hủy.
- Admin table phải có state không có dữ liệu và lỗi tải dữ liệu.

---

## 11. Nội dung mẫu dùng để tạo prototype

### 10.1 Người dùng mẫu

- Họ tên: Trần Minh An.
- Email: minhan@example.com.
- Gói hiện tại: Free.
- Lượt phân tích còn lại: 2/3.
- Vị trí mục tiêu mặc định: Frontend Developer.

### 10.2 CV mẫu

- Tên file: `Tran_Minh_An_Frontend_CV.pdf`.
- Dung lượng: 1.8 MB.
- Vị trí mục tiêu: Frontend Developer.
- Ngày phân tích: 10/07/2026.
- Tổng điểm: 72/100.
- Xếp loại: Khá.

### 10.3 Điểm thành phần mẫu

| Tiêu chí | Điểm |
| --- | ---: |
| Bố cục | 82 |
| Nội dung | 68 |
| Từ khóa | 70 |
| Văn phong | 74 |
| ATS | 66 |

### 10.4 Lỗi mẫu

1. **Cần ưu tiên — Thiếu kết quả định lượng**  
   Hai mô tả dự án chỉ nêu nhiệm vụ, chưa thể hiện kết quả hoặc mức độ đóng góp.

2. **Cần ưu tiên — Thông tin thời gian chưa nhất quán**  
   Có mốc thời gian kinh nghiệm cần kiểm tra lại để tránh gây hiểu nhầm.

3. **Nên cải thiện — Định dạng ngày tháng không đồng nhất**  
   Một số mục dùng `MM/YYYY`, một số mục dùng tên tháng bằng chữ.

4. **Nên cải thiện — Thiếu từ khóa nền tảng**  
   CV chưa thể hiện rõ REST API và Git trong phần kỹ năng dù có xuất hiện trong dự án.

5. **Đã làm tốt — Cấu trúc mục rõ ràng**  
   Các phần Học vấn, Kỹ năng, Dự án và Kinh nghiệm được phân tách dễ đọc.

### 10.5 Gợi ý mẫu

- Bổ sung số liệu cụ thể cho dự án, ví dụ số người dùng, thời gian xử lý hoặc tỷ lệ cải thiện.
- Thống nhất định dạng tháng/năm trong toàn bộ CV.
- Đưa kỹ năng thực sự đã sử dụng vào phần Kỹ năng và mô tả rõ trong dự án liên quan.
- Rút ngắn câu mô tả, bắt đầu bằng động từ hành động.
- Kiểm tra lại toàn bộ mốc thời gian trước khi ứng tuyển.

### 10.6 Câu mẫu Premium mock

**Hiện tại:** “Tham gia phát triển giao diện website bán hàng bằng React.”

**Gợi ý:** “Phát triển 8 màn hình responsive bằng React và tối ưu luồng hiển thị sản phẩm, giúp giảm thời gian tải trang trong môi trường kiểm thử nội bộ.”

**Lưu ý:** Chỉ giữ lại số liệu nếu đúng với trải nghiệm thực tế của người dùng.

---

## 12. Quy tắc về quyền riêng tư và niềm tin

CV chứa thông tin cá nhân. Prototype phải thể hiện rõ các nguyên tắc sau:

- Luôn xin sự đồng ý trước khi tải và phân tích CV.
- Không dùng CV để huấn luyện lại mô hình nếu chưa có sự đồng ý riêng.
- Người dùng có quyền yêu cầu xóa dữ liệu CV.
- Chỉ người dùng sở hữu CV mới được xem kết quả.
- Không hiển thị CV thật trong mockup công khai.
- Dùng dữ liệu giả trong prototype.
- Các cảnh báo mâu thuẫn phải trung lập, không gắn nhãn “gian dối”.

Khối “An toàn dữ liệu” nên xuất hiện ở:

- Landing Page.
- Upload screen.
- Hồ sơ cá nhân → Dữ liệu & quyền riêng tư.

---

## 13. Responsive và accessibility

### Desktop

- Thiết kế ưu tiên trước ở khung 1440 px.
- Dashboard và result page có thể dùng layout 2 cột.
- Admin dùng sidebar + content table.

### Tablet

- Các card co về một cột hoặc hai cột cân bằng.
- Table admin có horizontal scroll.
- Sidebar có thể thu gọn.

### Mobile

- Thiết kế ở khung 390 px.
- Navigation chuyển thành menu hoặc bottom navigation.
- Score card lên trước, issue list theo sau.
- CTA chính sticky ở cuối màn hình ở bước Upload/Chọn vị trí nếu cần.
- Không thu nhỏ table admin thành chữ quá nhỏ; dùng card list hoặc scroll.

### Accessibility

- Độ tương phản đạt WCAG AA.
- Focus state rõ ràng.
- Mọi input có label.
- Icon có text hoặc tooltip.
- Không chỉ dùng màu để báo lỗi/mức độ.
- Modal có thứ tự focus hợp lý.
- Nút bấm tối thiểu 44×44 px trên mobile.

---

## 14. Quy tắc bắt buộc cho Figma Make

### Luôn phải làm

- Tạo prototype bằng tiếng Việt.
- Giữ đúng trọng tâm MVP: tải CV → chọn vị trí → phân tích → xem điểm/lỗi → xem gợi ý tổng quan.
- Dùng dữ liệu mock đã cung cấp để giao diện có trạng thái thực tế.
- Tạo đầy đủ màn hình cho Guest, Registered User, Premium User và Admin theo danh sách Use Case.
- Mọi trang phải có loading, empty hoặc error state khi phù hợp.
- Hiển thị rõ thông báo quyền riêng tư tại bước Upload.
- Hiển thị rõ format file và giới hạn 5 MB.
- Hiển thị stepper trong luồng phân tích.
- Hiển thị điểm theo thang 0–100.
- Dùng đúng 5 tiêu chí: Bố cục, Nội dung, Từ khóa, Văn phong, ATS.
- Tạo Premium locked state nhưng không biến thành luồng AI Assistant.
- Tạo layout responsive cho desktop và mobile cho các màn hình người dùng chính.
- Dùng Auto Layout, component variants và design tokens nhất quán.

### Không được làm

- Không thêm Job Description vào luồng phân tích MVP.
- Không tạo Matching Score.
- Không tạo Skill Gap hoặc Keyword Gap theo JD.
- Không tạo Roadmap.
- Không tạo chatbot AI.
- Không tạo trình chỉnh sửa CV.
- Không tích hợp thanh toán/VNPay thật; chỉ tạo luồng VNPay mô phỏng theo UC 026.
- Không tạo chức năng tìm việc hoặc nộp đơn.
- Không thêm dashboard doanh nghiệp/nhà tuyển dụng.
- Không dùng dữ liệu cá nhân thật.
- Không thiết kế kết quả chấm điểm như một kết luận tuyệt đối về năng lực người dùng.
- Không làm giao diện quá giống các hệ thống quản trị nội bộ khô cứng ở phần người dùng cuối.

---

## 15. Ánh xạ Use Case sang màn hình

| Use Case | Tên | Màn hình/Component |
| --- | --- | --- |
| UC 001 | Quản lý danh sách role IT | AD01 |
| UC 002 | Quản lý điểm số của các skill | AD02 |
| UC 004 | Quản lý người dùng | AD03 |
| UC 008 | Đăng ký | P02, P02A |
| UC 009 | Đăng nhập | P03, P03A, P03B |
| UC 010 | Đăng xuất | P04, P05 |
| UC 011 | Quản lý thông tin cá nhân | U02 |
| UC 012 | Tải CV hệ thống | A01 |
| UC 013 | Chọn ngành nghề hoặc vị trí tiêu điểm | A02, A03 |
| UC 014 | Phân tích và chấm điểm CV | A04, A05 |
| UC 015 | Xem đánh giá kết quả CV | R01, R02, U03 |
| UC 016 | Xem gợi ý cải thiện CV | R03, R04, Premium modal |
| UC 026 | Xem gói dịch vụ | S01, S02 |

---

## 16. Trình tự tạo prototype đề xuất

Figma Make nên tạo theo thứ tự sau:

1. Design tokens và component nền tảng.
2. Landing Page.
3. Đăng ký, xác thực email, Đăng nhập và đặt lại mật khẩu.
4. Dashboard người dùng.
5. Upload CV.
6. Chọn vị trí mục tiêu.
7. Tiến trình phân tích.
8. Tổng quan kết quả.
9. Chi tiết lỗi.
10. Gợi ý cải thiện.
11. Premium locked/open state.
12. Hồ sơ cá nhân và xóa dữ liệu.
13. Lịch sử phân tích tối thiểu.
14. Gói dịch vụ và thanh toán VNPay mô phỏng.
15. Ba màn hình Admin.
16. Responsive mobile cho luồng chính.
17. Prototype links và các trạng thái lỗi/loading.

---

## 17. Tiêu chí hoàn thành prototype

Prototype được xem là đúng yêu cầu khi:

- Người xem có thể đi xuyên suốt luồng từ Landing Page đến kết quả CV.
- Luồng đăng ký có đồng ý điều khoản, xác thực email và gửi lại email xác thực.
- Luồng đăng nhập có ghi nhớ đăng nhập, quên mật khẩu và xử lý phiên hết hạn.
- Có bước đồng ý xử lý dữ liệu trước khi upload.
- Có chọn vị trí mục tiêu.
- Có progress state phân tích.
- Có score 0–100 và 5 tiêu chí thành phần.
- Có lỗi phổ biến, cảnh báo mâu thuẫn và gợi ý tổng quan.
- Có trạng thái Free/Premium rõ ràng nhưng không mở rộng sai phạm vi.
- Có hồ sơ cá nhân và luồng xóa dữ liệu.
- Có màn hình gói dịch vụ và luồng thanh toán VNPay mô phỏng, không phát sinh giao dịch thật.
- Có đủ ba màn hình quản trị, gồm các trạng thái chỉnh sửa/ngưng Role IT, thêm/chỉnh sửa hàng loạt kỹ năng và khóa/mở khóa người dùng.
- Không xuất hiện Matching Score, JD input, Skill Gap, Roadmap hoặc AI Assistant như chức năng đang hoạt động.
- Giao diện có thể dùng để demo ý tưởng MVP cho giảng viên, thành viên nhóm và người dùng thử nghiệm.

