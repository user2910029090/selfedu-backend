from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import google.generativeai as genai
import os

app = FastAPI(title="SelfEdu_Ai API")

# API kalitni Render muhitidan o'qiymiz
api_key = os.getenv("GEMINI_API_KEY")

# API kalit mavjudligini tekshirish
if not api_key:
    raise ValueError("GEMINI_API_KEY muhit o'zgaruvchisi topilmadi!")

genai.configure(api_key=api_key)

# Modelni o'rnatish
# Agar "gemini-3.1-flash-lite" ishlamasa, "gemini-1.5-flash" dan foydalaning
try:
    model = genai.GenerativeModel('gemini-3.1-flash-lite')
except:
    model = genai.GenerativeModel('gemini-1.5-flash')

class AIChat(BaseModel):
    fan_nomi: str
    savol: str

@app.post("/chat")
async def chat_with_ai(data: AIChat):
    try:
        # Promptni shakllantirish
        prompt = f"Fan: {data.fan_nomi}. Savol: {data.savol}"
        
        # AI dan javob olish
        response = model.generate_content(prompt)
        
        return {
            "fan": data.fan_nomi,
            "ai_javobi": response.text
        }
    except Exception as e:
        return {"xatolik": str(e)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)