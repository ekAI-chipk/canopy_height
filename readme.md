# Thư mục `process_data`

Thư mục này chứa các file `.py` phục vụ cho việc xử lý dữ liệu **GEDI** và **Sentinel-2**.

---

## 1. `unzip_file.py`

**Chức năng:**  
Giải nén các file `.zip` đã tải về từ Google Drive.

**Tham số đầu vào từ terminal:**

- `folder_path`: Đường dẫn tới thư mục chứa các file `.zip`.
- `extract_folder_path`: Đường dẫn tới thư mục đích để giải nén các file vào.

---

## 2. `crop_images.py`

**Chức năng:**  
Cắt ảnh Sentinel-2 và GEDI thành các patch nhỏ kích thước 15x15 pixel.

**Tham số đầu vào từ terminal:**

- `data_folder`: Thư mục chứa dữ liệu Sentinel-2 và GEDI.
- `crop_folder_path`: Đường dẫn tới thư mục lưu các patch đã được cắt.

---

## 3. `creat_h5file.py`

**Chức năng:**  
Tạo các file `.h5` từ các patch đã được crop.

**Tham số đầu vào từ terminal:**

- `data_folder`: Thư mục lưu các patch.
- `output_folder`: Thư mục lưu các file `.h5` đầu ra.

---

## 4. `group_h5file.py`

**Chức năng:**  
Chia các file `.h5` đã tạo thành 3 nhóm: `train`, `test`, `val` để sử dụng trong huấn luyện và đánh giá mô hình.

**Cách sử dụng:**
- Cần chỉnh sửa trực tiếp trong file các biến sau:
  - `source_folder`: Thư mục chứa các file `.h5` gốc.
  - `base_folder`: Thư mục chứa các thư mục con `val/`, `test/`, `train/` để phân chia file `.h5` vào.

---

## 5. `replace_zeros.py`

**Chức năng:**  
Thay thế các giá trị bằng `0` thành `NaN` trong dữ liệu GEDI của các file `.h5` — dùng khi dữ liệu bị xử lý sai (ví dụ như các pixel không có dữ liệu bị gán bằng `0`).

---
# Thư mục `download_data`

Thư mục này chứa **duy nhất một file Jupyter Notebook (.ipynb)** dùng để tải ảnh GEDI và Sentinel-2 từ Google Earth Engine (GEE) về Google Drive.

## Nội dung:
- **File notebook** thực hiện việc:
  - Truy cập và xử lý ảnh vệ tinh từ GEE.
  - Lưu kết quả (ảnh GEDI và Sentinel-2) vào Google Drive để sử dụng trong các bước xử lý dữ liệu tiếp theo.

---

# Thư mục `global_canopy_height`

Thư mục này chứa **source code chính** cho việc huấn luyện mô hình dự đoán chiều cao tán cây toàn cầu từ dữ liệu ảnh vệ tinh.

## Nội dung:
- Các script Python phục vụ:
  - Định nghĩa kiến trúc mô hình.
  - Thiết lập các tham số huấn luyện (optimizer, loss function,...).
  - Thực hiện huấn luyện, kiểm thử, và đánh giá mô hình.
  - Lưu mô hình đã huấn luyện và tạo ra bản đồ dự đoán chiều cao.

---


