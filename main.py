import uvicorn
import torch
import yaml
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from omegaconf import OmegaConf
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class LanguageDetection:
    def __init__(self, config_path: str):
        self.cfg = OmegaConf.load(config_path)
        print(f"Đang tải model từ: {self.cfg.model_path}...")

        self.tokenizer = AutoTokenizer.from_pretrained(self.cfg.model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.cfg.model_path)
        print("Model đã sẵn sàng!")

    def __call__(self, text: str):
        inputs = self.tokenizer(
            text, 
            padding=True, 
            truncation=True, 
            return_tensors="pt"
        )

        with torch.no_grad():
            outputs = self.model(**inputs)

        idx = outputs.logits.argmax(-1).item()
        return self.model.config.id2label[idx]

app = FastAPI(title="Language Detection API by Bao")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

try:
    classifier = LanguageDetection("config.yaml")
except Exception as e:
    print(f"Lỗi khi khởi tạo model: {e}")
    classifier = None

class TextRequest(BaseModel):
    text: str


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

if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=8000)