# 🎨 Tkinter GUI - Hướng Dẫn Khởi Động Nhanh

## 🚀 Khởi Động Ứng Dụng

### Cách 1: Chạy trực tiếp
```bash
python main_gui.py
```

### Cách 2: Từ Python shell
```python
from main_gui import main
main()
```

### Cách 3: Chạy file test trước
```bash
python test_gui.py
```

## 🎯 Các Tính Năng Chính

### 1️⃣ Đăng Nhập / Đăng Ký
- **Email**: thien@example.com
- **Mật khẩu**: Minimum 6 characters
- **Khôi phục mật khẩu**: Click "FORGOT PASSWORD"
- **Xem liên lạc**: Click "BROWSE AS GUEST"

### 2️⃣ Quản Lý Liên Lạc
| Chức năng | Mô tả |
|-----------|-------|
| **Thêm** | Tạo liên lạc mới với đầy đủ thông tin |
| **Xem tất cả** | Hiển thị bảng tất cả liên lạc |
| **Tìm kiếm** | Tìm theo tên/điện thoại/email/nhóm |
| **Chỉnh sửa** | Cập nhật thông tin liên lạc |
| **Xóa** | Xóa liên lạc (xác nhận trước) |

### 3️⃣ Quản Lý Nhóm
```
Tạo Nhóm → Thêm Liên Lạc vào Nhóm → Quản Lý
```

### 4️⃣ Nhập/Xuất
- **Xuất**: Lưu liên lạc thành JSON
- **Nhập**: Tải từ file JSON
- **Lịch sử**: Xem tất cả thao tác

### 5️⃣ Thông Báo
- Tự động sinh nhật
- Xem tất cả / Chưa đọc
- Đánh dấu là đã đọc

### 6️⃣ Hồ Sơ
- Xem thông tin hiện tại
- Cập nhật tên, email, điện thoại

## 🎨 Bảng Màu Chuyên Nghiệp

```
🔵 Xanh (#2E86AB)    - Header, nút chính
🟣 Tím (#A23B72)     - Đăng ký
🟠 Cam (#F18F01)     - Nhập/Xuất
🟢 Xanh (#06A77D)    - Nhóm
🔴 Đỏ (#C1121F)      - Xóa
```

## ⌨️ Phím Tắt

| Phím | Chức năng |
|------|----------|
| `Ctrl+C` | Thoát ứng dụng |
| `Tab` | Chuyển giữa các trường |
| `Enter` | Xác nhận / Đăng nhập |

## 💾 Lưu Trữ Dữ Liệu

Tất cả dữ liệu được lưu trong thư mục `data/`:

```
📁 data/
├── 👤 users.json              (Tài khoản)
├── 📞 contacts.json           (Liên lạc)
├── 📂 groups.json             (Nhóm)
├── 📬 notifications.json      (Thông báo)
└── 📋 import_export_history.json (Lịch sử)
```

## 🔒 Bảo Mật

✅ SHA-256 password hashing  
✅ Email validation  
✅ Mật khẩu tối thiểu 6 ký tự  
✅ Ngăn chặn trùng lặp  

## 📝 Ví Dụ Sử Dụng

### Tạo Liên Lạc Mới
1. Đăng nhập
2. Click "Contacts" → "Add Contact"
3. Nhập:
   - Tên: Trần Văn A
   - Điện thoại: 0912345678
   - Email: tran.van.a@gmail.com
   - Địa chỉ: 123 Đường ABC (tùy chọn)
   - Sinh nhật: 1990-05-15 (tùy chọn)
4. Click "ADD CONTACT"

### Tìm Kiếm Liên Lạc
1. Click "Contacts" → "Search"
2. Chọn loại tìm kiếm
3. Nhập từ khóa
4. Click "SEARCH"

### Tạo Nhóm
1. Click "Groups" → "Create Group"
2. Nhập tên nhóm: "Bạn"
3. Click "CREATE"

### Thêm vào Nhóm
1. Click "Groups" → "Add to Group"
2. Nhập Contact ID
3. Nhập tên nhóm
4. Click "ADD"

### Xuất Liên Lạc
1. Click "Import/Export" → "Export All"
2. Chọn vị trí lưu
3. File được lưu dưới dạng JSON

## 🐛 Khắc Phục Sự Cố

### Lỗi: ModuleNotFoundError
```bash
pip install pillow  # Nếu cần
python main_gui.py
```

### Ứng dụng không mở
- Kiểm tra Python 3.7+
- Kiểm tra tkinter cài đặt
- Chạy `python test_gui.py` để test

### Dữ liệu không lưu
- Kiểm tra thư mục `data/` tồn tại
- Kiểm tra quyền ghi file

## 📚 Tài Liệu Thêm

- 📖 [GUI_README.md](GUI_README.md) - Hướng dẫn chi tiết
- 📖 [README.md](README.md) - Tài liệu chính
- 📖 [API_REFERENCE.md](API_REFERENCE.md) - Tài liệu API

## 💡 Mẹo

1. **Tìm kiếm từng phần**: "Thị" sẽ tìm "Trần Thị Hương"
2. **Nhóm linh hoạt**: Một liên lạc có thể ở nhiều nhóm
3. **Sao lưu thường xuyên**: Xuất liên lạc định kỳ
4. **Kiểm tra sinh nhật**: Hệ thống tự động thông báo

## ✨ Đặc Điểm Nổi Bật

✅ Giao diện hiện đại, thân thiện  
✅ Đầy đủ chức năng quản lý  
✅ Bảo mật cao  
✅ Dữ liệu lưu cục bộ  
✅ Không cần Internet  
✅ Dễ sử dụng  

---

**Phiên bản**: 2.0 GUI  
**Trạng thái**: ✅ Hoạt động đầy đủ
