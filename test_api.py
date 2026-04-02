import requests

# http://127.0.0.1:8000
# Nếu muốn test link Public (Pinggy), hãy dán link đó vào đây.
BASE_URL = "http://127.0.0.1:8000"

def test_root():
    print("--- Kiểm tra Endpoint GET / ---")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_health():
    print("--- Kiểm tra Endpoint GET /health ---")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_predict(text_input):
    print(f"--- Kiểm tra Endpoint POST /predict với văn bản: '{text_input}' ---")
    payload = {"text": text_input}
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    
    if response.status_code == 200:
        print("Kết quả dự đoán:", response.json()["data"]["detected_language"])
    else:
        print("Lỗi:", response.json()["detail"])
    print(f"Full JSON: {response.json()}\n")

if __name__ == "__main__":
    # Chạy các bài test
    try:
        test_root()
        test_health()
        
        # Test ít nhất 2 dữ liệu đầu vào theo yêu cầu của thầy 
        test_predict("Chào thầy, em là Gia Bảo!")
        test_predict("Hello, this is a language detection test.")
        
    except requests.exceptions.ConnectionError:
        print("LỖI: Không thể kết nối đến Server. Bảo nhớ chạy file main.py trước nhé!")