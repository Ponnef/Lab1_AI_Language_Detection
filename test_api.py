import requests

BASE_URL = "http://127.0.0.1:8000"

def test_root():
    print("1. Kiểm tra Endpoint GET /")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}\n")
    except Exception as e:
        print(f"Lỗi: {e}\n")

def test_health():
    print("2. Kiểm tra Endpoint GET /health")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}\n")
    except Exception as e:
        print(f"Lỗi: {e}\n")

def test_predict(text_input):
    print(f"3. Kiểm tra POST /predict với văn bản: '{text_input}'")
    payload = {"text": text_input}
    try:
        response = requests.post(f"{BASE_URL}/predict", json=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Kết quả dự đoán: {result['language']}")
            print(f"Trạng thái: {result['status']}")
        else:
            print(f"Lỗi từ server: {response.json().get('detail', 'Không xác định')}")
        
        print(f"Full JSON: {response.json()}\n")
    except Exception as e:
        print(f"Lỗi kết nối: {e}\n")

if __name__ == "__main__":
    print("BẮT ĐẦU KIỂM THỬ API\n")
    
    try:
        test_root()
        test_health()
        
        # Test 1: Tiếng Việt
        test_predict("Chào thầy, em là Gia Bảo, mssv 24120264.")
        
        # Test 2: Tiếng Anh
        test_predict("Artificial Intelligence is a very interesting field of study.")
        
        # Test 3: Trường hợp lỗi (Gửi text rỗng để test xử lý lỗi)
        test_predict("   ")

    except requests.exceptions.ConnectionError:
        print("LỖI: Không thể kết nối đến Server")
    
    print("HOÀN TẤT")