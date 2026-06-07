from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import google.generativeai as genai
import os

app = FastAPI(title="SelfEdu_Ai API")

# API kalitni Render muhitidan o'qiymiz
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Modelni o'rnatish
try:
    model = genai.GenerativeModel('gemini-1.5-flash') # 3.1 versiyasi hali hamma uchun ochiq bo'lmasligi mumkin
except:
    model = genai.GenerativeModel('gemini-pro')

class AIChat(BaseModel):
    fan_nomi: str
    savol: str

# ASOSIY SAHIFA UCHUN (404 xatosini yo'qotadi)
@app.get("/")
async def root():
    return {"message": "SelfEdu_AI serveri ishlamoqda!"}

@app.post("/chat")
async def chat_with_ai(data: AIChat):
    try:
        response = model.generate_content(f"Fan: {data.fan_nomi}. Savol: {data.savol}")
        return {"ai_javobi": response.text}
    except Exception as e:
        return {"xatolik": str(e)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)