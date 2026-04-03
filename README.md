# Language Detection API Service
### Thông tin sinh viên
* ### Họ và Tên: Nguyễn Huỳnh Gia Bảo
* ### MSSV: 24120264
* ### Lớp/Khóa: 24CTT3/K24
### **Tên mô hình và liên kết HF**
* **Tên mô hình:** XLM-RoBERTa Base for Language Detection
* **Liên kết Hugging Face:** https://huggingface.co/papluca/xlm-roberta-base-language-detection
 
### **Mô tả ngắn về chức năng của hệ thống**
* Hệ thống cung cấp một API nhận diện ngôn ngữ của văn bản đầu vào dựa trên kiến trúc mô hình học sâu **XLM-RoBERTa**. Người dùng có thể gửi một đoạn văn bản (Tiếng Việt, Tiếng Anh, Tiếng Nhật,...) 
qua hệ thống API, máy chủ sẽ tiến hành trích xuất đặc trưng ngôn ngữ và trả về mã nhãn dự đoán tương ứng (như `vi`, `en`, `ja`) với độ chính xác cao dựa trên mô hình đã được huấn luyện sẵn trên đa ngôn ngữ

### **Hướng dẫn cài đặt thư viện**
* Yêu cầu máy tính đã cài đặt sẵn Python. Để cài đặt các thư viện cần thiết, hãy chạy lệnh sau trong terminal tại thư mục gốc của project:
```bash
pip install -r requirements.txt
```
### Hướng dẫn chạy chương trình
1. Mở terminal tại thư mục gốc của project
2. Khởi chạy server FastAPI bằng lệnh  uvicorn:
``` bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
3. Sau khi chạy lệnh này, server sẽ bắt đầu lắng nghe tại địa chỉ http://127.0.0.1:8000.
### Hướng dẫn gọi API và ví dụ request/response
1. Get / (root)
*  Chức năng: Trả về thông tin giới thiệu và thông tin sinh viên.
*  Request mẫu:
``` bash
import requests
url = "http://127.0.0.1:8000/"
response = requests.get(url)
print(response.json())
```
*  Response mẫu:
```bash
{
    "message": "Hệ thống nhận diện ngôn ngữ của Bảo",
    "mssv": "24120264"
}
```
2. Get /health
* Chức năng: Kiểm tra trạng thái hoạt động của server.
* Resquest mẫu:
``` bash
import requests
url = "http://127.0.0.1:8000/health"
response = requests.get(url)
response.json()
```
* Response mẫu:
``` bash
{
    "status": "ok"
}
```
3.  Get /classify
* Chức năng: Nhận diện ngôn ngữ nhanh qua tham số message trên URL (thích hợp test nhanh bằng trình duyệt).
* Request mẫu:
``` bash
import requests
url = "http://127.0.0.1:8000/classify"
payload = {"message": "hello baby"}
response = requests.get(url, params=payload)
response.json()
* Response mẫu:
``` bash
{
    "prediction": "en"
}
```
4. POST /predict
* Chức năng: Nhận văn bản qua JSON body, phân loại và trả về kết quả dự đoán nhãn ngôn ngữ.
* Request mẫu sử dụng Python (requests):
``` bash
import requests
url = "http://127.0.0.1:8000/predict"
payload = {"text": "Chào thầy, em là Gia Bảo!"}
response = requests.post(url, json=payload)
print(response.json())
```
* Response mẫu (Thành công):
``` bash
{
    "language": "vi",
    "status": "success"
}
```
* Response mẫu (Lỗi văn bản rỗng):
``` bash
{
    "detail": "Vui lòng nhập văn bản!"
}
```
### **🎥 Video demo**

