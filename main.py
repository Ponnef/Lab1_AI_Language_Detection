import uvicorn
import torch
import yaml
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from omegaconf import OmegaConf
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# --- 1. ĐỊNH NGHĨA CLASS MODEL ---
class LanguageDetection:
    def __init__(self, config_path: str):
        # Load config từ file yaml
        self.cfg = OmegaConf.load(config_path)
        print(f"Đang tải model từ: {self.cfg.model_path}...")
        
        # Khởi tạo Tokenizer và Model
        self.tokenizer = AutoTokenizer.from_pretrained(self.cfg.model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.cfg.model_path)
        print("✅ Model đã sẵn sàng!")

    def __call__(self, text: str):
        # Tiền xử lý đầu vào
        inputs = self.tokenizer(
            text, 
            padding=True, 
            truncation=True, 
            return_tensors="pt"
        )
        
        # Dự đoán không tính gradient (giảm bộ nhớ)
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        # Lấy nhãn ngôn ngữ từ logits
        idx = outputs.logits.argmax(-1).item()
        return self.model.config.id2label[idx]

# --- 2. KHỞI TẠO APP & MODEL ---
app = FastAPI(title="Language Detection API by Bao")

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Khởi tạo model (Đảm bảo có file config.yaml cùng thư mục)
try:
    classifier = LanguageDetection("config.yaml")
except Exception as e:
    print(f"❌ Lỗi khi khởi tạo model: {e}")
    classifier = None

# Schema cho POST request
class TextRequest(BaseModel):
    text: str

# --- 3. ĐỊNH NGHĨA CÁC ENDPOINTS ---

@app.get('/')
async def root():
    return {
        "message": "Hệ thống nhận diện ngôn ngữ của Bảo", 
        "mssv": "24120264"
    }

@app.get('/health')
async def health():
    return {"status": "ok"}

@app.get('/classify')
async def classify_get(message: str):
    """Sử dụng cho link Pinggy hoặc gọi nhanh qua trình duyệt"""
    if not message or not message.strip():
        raise HTTPException(status_code=400, detail="Message không được để trống!")
    
    if classifier is None:
        return {"error": "Model chưa được khởi tạo!"}

    try:
        label = classifier(message)
        return {"prediction": label}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/predict')
async def predict(request: TextRequest):
    """Cổng nộp bài chính thức qua POST"""
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Vui lòng nhập văn bản!")
    
    if classifier is None:
        raise HTTPException(status_code=500, detail="Model server error")

    res = classifier(request.text)
    return {"language": res, "status": "success"}

# --- 4. CHẠY SERVER ---
if __name__ == "__main__":
    # Chạy trực tiếp bằng: python main.py
    uvicorn.run(app, host="0.0.0.0", port=8000)