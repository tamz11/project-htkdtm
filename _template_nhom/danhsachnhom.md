# Danh Sách Nhóm Và Phân Công Nhiệm Vụ

## 1. Thông Tin Chung

- **Tên nhóm:** [Điền tên nhóm theo định dạng: tennhom-tenlop, ví dụ: nhom01-dhti15a1hn]
- **Tên lớp học phần:** [Điền mã hoặc tên lớp học phần]
- **Tên đề tài:** [Điền tên đề tài đồ án / bài tập lớn]
- **Giảng viên hướng dẫn:** [Điền tên giảng viên]

---

## 2. Danh Sách Thành Viên

| STT | Họ và Tên | Mã Sinh Viên | Lớp Sinh Hoạt | Vai Trò | Nhiệm Vụ Phân Công | Tỷ Lệ Đóng Góp (%) | Email |
| :-: | :--- | :-: | :-: | :--- | :--- | :-: | :--- |
| 1 | [Nguyễn Văn A] | [20210001] | [DHTI15A1HN] | Nhóm trưởng | Thiết kế kiến trúc, phát triển Backend API | 100% | a@student.edu.vn |
| 2 | [Trần Thị B] | [20210002] | [DHTI15A1HN] | Thành viên | Thiết kế giao diện Frontend, tích hợp API | 100% | b@student.edu.vn |
| 3 | [Lê Văn C] | [20210003] | [DHTI15A1HN] | Thành viên | Thiết kế cơ sở dữ liệu, kiểm thử phần mềm | 100% | c@student.edu.vn |

---

## 3. Cấu Trúc Mã Nguồn Trong Thư Mục Nhóm

Mã nguồn của nhóm phải được đặt trong thư mục này theo cấu trúc khuyến nghị:

```text
<tennhom-tenlop>/
├── danhsachnhom.md        # Tệp tin thông tin nhóm này
├── README.md              # (Tùy chọn) Hướng dẫn cài đặt và chạy mã nguồn của riêng nhóm
├── docs/                  # Tài liệu phân tích, thiết kế, báo cáo đồ án
│   └── baocao.pdf
└── src/                   # Mã nguồn của dự án
    ├── backend/
    └── frontend/
```

---

## 4. Hướng Dẫn Cài Đặt Và Thực Thi Mã Nguồn

### 4.1. Môi trường yêu cầu

Để cài đặt và vận hành hệ thống, cần chuẩn bị các môi trường và công cụ sau:

- **Hệ điều hành:** Windows 10/11 hoặc Ubuntu 22.04 trở lên.
- **Nền tảng thực thi:** Node.js >= 18.x, Python >= 3.10 hoặc JDK >= 17, tùy theo công nghệ sử dụng trong dự án.
- **Cơ sở dữ liệu:** PostgreSQL, MySQL hoặc MongoDB tùy theo cấu hình hệ thống.
- **Công cụ hỗ trợ:** Git để quản lý mã nguồn, Visual Studio Code để chỉnh sửa và phát triển ứng dụng.
- **Kết nối Internet:** Đảm bảo kết nối mạng ổn định để tải mã nguồn và cài đặt các thư viện cần thiết.

### 4.2. Các bước cài đặt và khởi chạy

**Bước 1: Tải mã nguồn và cấu hình môi trường**

Sử dụng Git để clone mã nguồn từ repository về máy tính. Sau khi tải thành công, truy cập vào thư mục dự án và mở bằng Visual Studio Code. Tiến hành kiểm tra các tệp cấu hình, sao chép tệp cấu hình mẫu (nếu có) và khai báo các thông số cần thiết như thông tin kết nối cơ sở dữ liệu, cổng chạy ứng dụng và các biến môi trường liên quan.

**Bước 2: Cài đặt các gói phụ thuộc**

Tiến hành cài đặt các thư viện và gói phụ thuộc được sử dụng trong dự án thông qua công cụ quản lý tương ứng như npm, pip hoặc Maven. Đảm bảo các thư viện được cài đặt đầy đủ, đúng phiên bản và không phát sinh lỗi trong quá trình cài đặt.

**Bước 3: Khởi tạo cơ sở dữ liệu**

Thiết lập cơ sở dữ liệu theo cấu hình của hệ thống, kiểm tra thông tin kết nối và thực hiện khởi tạo cấu trúc dữ liệu nếu cần. Đảm bảo cơ sở dữ liệu hoạt động ổn định và sẵn sàng phục vụ các thao tác truy vấn, lưu trữ dữ liệu của ứng dụng.

**Bước 4: Khởi chạy ứng dụng**

Sau khi hoàn tất cấu hình và cài đặt, thực hiện lệnh khởi chạy ứng dụng tại thư mục dự án. Kiểm tra các thông báo trên Terminal để xác nhận hệ thống đã khởi động thành công, đồng thời truy cập vào địa chỉ ứng dụng được cung cấp để bắt đầu sử dụng.

**Bước 5: Kiểm tra hoạt động**

Tiến hành kiểm tra giao diện, các chức năng chính, khả năng kết nối cơ sở dữ liệu và quá trình xử lý dữ liệu. Nếu phát sinh lỗi, cần kiểm tra lại cấu hình môi trường, các gói phụ thuộc và thông báo lỗi để khắc phục. Sau khi các chức năng hoạt động ổn định, hệ thống sẵn sàng đưa vào sử dụng và thử nghiệm.

