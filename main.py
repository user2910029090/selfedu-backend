from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os

app = FastAPI(title="SelfEdu_Ai API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Render'dan olingan kalitni o'qiydi
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

class AIChat(BaseModel):
    fan_nomi: str
    savol: str

@app.get("/")
async def root():
    return {"message": "AI serveri ishlamoqda!"}

@app.post("/chat")
async def chat_with_ai(data: AIChat):
    prompt = f"Fan: {data.fan_nomi}. Savol: {data.savol}. Qisqa va tushunarli javob ber."
    response = model.generate_content(prompt)
    return {"ai_javobi": response.text}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)