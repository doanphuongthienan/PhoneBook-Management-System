# Phone Book Management System - Tkinter GUI Guide

## 🎨 Giao Diện Tkinter Đầy Đủ Chức Năng

Hệ thống Phone Book Management System hiện có giao diện Tkinter hiện đại và thân thiện với người dùng.

## 📋 Các Tính Năng Giao Diện

### 1. **Màn Hình Đăng Nhập**
- Đăng nhập bằng email và mật khẩu
- Đăng ký tài khoản mới
- Khôi phục mật khẩu
- Xem liên lạc ở chế độ khách

### 2. **Bảng Điều Khiển Chính**
- Hiển thị chào mừng người dùng
- 6 tùy chọn chính:
  - Quản lý Liên Lạc
  - Quản lý Nhóm
  - Nhập/Xuất
  - Thông Báo
  - Hồ Sơ
  - Đăng Xuất

### 3. **Quản Lý Liên Lạc**
- **Thêm liên lạc mới**
  - Nhập tên, điện thoại, email
  - Thêm địa chỉ (tùy chọn)
  - Thiết lập ngày sinh nhật
  - Thêm ghi chú

- **Xem tất cả liên lạc**
  - Hiển thị dưới dạng bảng
  - Các cột: ID, Tên, Điện thoại, Email, Nhóm

- **Tìm kiếm liên lạc**
  - Tìm kiếm theo: Tất cả, Tên, Điện thoại, Email, Nhóm
  - Tìm kiếm không phân biệt chữ hoa chữ thường
  - Tìm kiếm từng phần

- **Chỉnh sửa liên lạc**
  - Cập nhật thông tin liên lạc
  - Thay đổi bất kỳ trường nào

- **Xóa liên lạc**
  - Xác nhận trước khi xóa
  - Không thể phục hồi

### 4. **Quản Lý Nhóm**
- **Tạo nhóm mới**
  - Đặt tên nhóm
  - Lưu trữ cho tài khoản của bạn

- **Xem nhóm**
  - Liệt kê tất cả các nhóm
  - Hiển thị số lượng liên lạc trong mỗi nhóm

- **Thêm liên lạc vào nhóm**
  - Nhập ID liên lạc
  - Nhập tên nhóm

- **Xóa liên lạc khỏi nhóm**
  - Xóa mà không xóa liên lạc

- **Xóa nhóm**
  - Xóa nhóm (giữ lại liên lạc)

### 5. **Nhập/Xuất**
- **Xuất tất cả liên lạc**
  - Lưu thành file JSON
  - Hộp thoại chọn vị trí lưu

- **Xuất theo nhóm**
  - Chọn nhóm
  - Xuất liên lạc của nhóm

- **Nhập liên lạc**
  - Chọn file JSON
  - Tự động kiểm tra trùng lặp
  - Xác nhận kết quả nhập

- **Xem lịch sử**
  - Xem tất cả thao tác nhập/xuất
  - Hiển thị ngày, hành động, tệp, số lượng, trạng thái

### 6. **Thông Báo**
- **Xem tất cả thông báo**
- **Xem thông báo chưa đọc**
- **Đánh dấu là đã đọc**
- **Xóa tất cả thông báo**
- Bao gồm thông báo sinh nhật tự động

### 7. **Quản Lý Hồ Sơ**
- Xem thông tin hiện tại
- Cập nhật tên đầy đủ
- Cập nhật email
- Cập nhật điện thoại
- Lưu thay đổi

## 🎨 Bảng Màu

Hệ thống sử dụng bảng màu chuyên nghiệp:

| Màu | Mã | Sử Dụng |
|-----|-----|--------|
| Xanh Dương Chính | #2E86AB | Header, nút chính |
| Tím Thứ Cấp | #A23B72 | Đăng ký, thay thế |
| Cam Nhấn | #F18F01 | Nhập/Xuất, cảnh báo |
| Xanh Lá Thành Công | #06A77D | Nhóm, thành công |
| Đỏ Nguy Hiểm | #C1121F | Xóa, lỗi |
| Tối | #1A1A1A | Nền tối |
| Sáng | #F5F5F5 | Nền chính |
| Văn Bản | #333333 | Màu chữ |

## 🚀 Chạy Ứng Dụng GUI

### Từ Terminal:
```bash
python main_gui.py
```

### Hoặc chạy từ Python:
```python
from ui.tkinter_gui import PhoneBookApp

app = PhoneBookApp()
app.mainloop()
```

## 📦 Yêu Cầu

- Python 3.7+
- tkinter (đi kèm với Python)
- Pillow (tùy chọn): `pip install Pillow`

## 💡 Mẹo Sử Dụng

1. **Tìm kiếm hiệu quả**
   - Tìm kiếm không phân biệt chữ hoa chữ thường
   - Tìm kiếm từng phần (ví dụ: "Thị" sẽ tìm thấy "Trần Thị Hương")

2. **Quản lý nhóm**
   - Một liên lạc có thể thuộc nhiều nhóm
   - Xóa nhóm không ảnh hưởng đến liên lạc

3. **Sao lưu dữ liệu**
   - Sử dụng tính năng xuất để tạo bản sao lưu JSON
   - Nhập từ các tệp trước đó khi cần

4. **Thông báo sinh nhật**
   - Hệ thống tự động kiểm tra sinh nhật
   - Nhập ngày sinh dưới định dạng: YYYY-MM-DD

## 🔒 Bảo Mật

- Mật khẩu được mã hóa bằng SHA-256
- Mật khẩu phải có ít nhất 6 ký tự
- Email được xác thực theo RFC standard
- Dữ liệu lưu trữ cục bộ trong JSON

## 📝 Cấu Trúc Dữ Liệu

Tất cả dữ liệu được lưu trữ trong thư mục `data/`:

```
data/
├── users.json                    # Thông tin người dùng
├── contacts.json                 # Thông tin liên lạc
├── groups.json                   # Thông tin nhóm
├── notifications.json            # Thông báo
└── import_export_history.json   # Lịch sử thao tác
```

## 🐛 Khắc Phục Sự Cố

### Tkinter không được cài đặt
**Windows:**
```bash
python -m pip install tk
```

**macOS:**
```bash
brew install python-tk
```

**Linux:**
```bash
sudo apt-get install python3-tk
```

### Lỗi khi nhập file
- Đảm bảo file JSON hợp lệ
- Kiểm tra cấu trúc file theo format standard
- Hệ thống sẽ báo lỗi chi tiết nếu có vấn đề

### Ứng dụng chạy chậm
- Giảm số lượng thông báo (xóa cũ)
- Xuất/nhập để tạo file mới sạch
- Đóng các ứng dụng khác

## 📚 Thêm Tài Liệu

- Xem `README.md` cho hướng dẫn chi tiết
- Xem `API_REFERENCE.md` cho tài liệu API
- Xem `QUICK_START.md` cho khởi động nhanh

## 👨‍💻 Phát Triển Thêm

Giao diện Tkinter được thiết kế để dễ mở rộng:

1. **Thêm tính năng mới**
   - Tạo lớp Frame mới kế thừa từ BaseFrame
   - Sử dụng các dịch vụ hiện có

2. **Tùy chỉnh giao diện**
   - Sửa COLORS dict trong tkinter_gui.py
   - Thay đổi kích thước, font chữ

3. **Thêm nút/chức năng**
   - Sử dụng `create_button()` method
   - Kết nối với dịch vụ backend

## 📞 Hỗ Trợ

Nếu gặp vấn đề:
1. Kiểm tra lỗi trong terminal
2. Xem file log nếu có
3. Đảm bảo tất cả dữ liệu files tồn tại

---

**Phiên bản**: 2.0  
**Ngôn ngữ giao diện**: Tkinter  
**Trạng thái**: Hoạt động đầy đủ ✅
