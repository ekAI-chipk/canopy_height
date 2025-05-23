# Global Canopy Height

## Requirements

```bash
conda create -n chme python=3.10
conda activate chme
pip install -r global_canopy_height/requirements.txt
conda install -c conda-forge gdal
```

## Data

### 1. Tải dữ liệu S2 và GEDI từ Google Earth Engine (GEE) về Google Drive
- **Sử dụng notebook**: `download_data/download_data.ipynb`
- **Chức năng**: Tải ảnh Sentinel-2 (S2) và dữ liệu GEDI từ GEE và lưu vào Google Drive.

### 2. Tải dữ liệu S2 và GEDI từ Google Drive dưới dạng `.zip` và giải nén

- **Sử dụng script**: `python process_data/unzip_file.py`
- **Chức năng**: Giải nén các file `.zip` đã tải từ Google Drive về.
- **Tham số đầu vào từ terminal**:
  - `Folder_path`: đường dẫn tới thư mục chứa các file `.zip`
  - `Extract_folder_path`: đường dẫn tới thư mục đích để giải nén các file

### 4. Tạo các file `.h5` từ các patch

- **Sử dụng script**: `process_data/creat_h5file.py`
- **Chức năng**: Tạo các file `.h5` từ các patch đã được crop.
- **Tham số đầu vào từ terminal**:
  - `Data_folder`: thư mục lưu trữ các patch
  - `Output_folder`: nơi lưu trữ các file `.h5` được tạo ra

### 5. Chia các file `.h5` thành các tập train, test, val

- **Sử dụng script**: `process_data/group_h5file.py`
- **Chức năng**: Phân chia các file `.h5` đã tạo vào các thư mục `train`, `val`, và `test` để phục vụ huấn luyện, xác thực và kiểm tra mô hình.
- **Yêu cầu chỉnh sửa trong code**:
  - `source_folder`: đường dẫn chứa các file `.h5` gốc
  - `base_folder`: đường dẫn chứa các thư mục con `train`, `val`, `test` để chia dữ liệu vào

## Training

Chạy script huấn luyện mô hình bằng lệnh sau:

```
bash global_canopy_height/gchm/bash/run_training.sh
```

## Deploying

Triển khai mô hình bằng cách chạy lệnh sau trong terminal:

```
bash global_canopy_height/gchm/bash/deploy_example.sh
```


