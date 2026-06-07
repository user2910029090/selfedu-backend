from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import google.generativeai as genai

app = FastAPI()

# CORS - Frontend bilan bog'lanish uchun
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# AI va Baza sozlamalari (Hammasi kommentariyaga olindi)
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# model = genai.GenerativeModel('gemini-1.5-flash')

# Bazaviy simulyatsiya uchun xotira
db_users = {} 

class UserAction(BaseModel):
    ism: str
    familiya: str = None
    fan: str = None
    savol: str = None
    ball: int = 0

# 1. Ro'yxatdan o'tish (Baza simulyatsiyasi)
@app.post("/register")
async def register(data: UserAction):
    db_users[data.ism] = {"familiya": data.familiya, "ball": 0}
    return {"message": f"{data.ism} tizimga qo'shildi", "status": "ok"}

# 2. Fanlar va Mavzular (Frontend uchun)
@app.get("/data")
async def get_data():
    return {
        "fanlar": ["Biologiya", "Tarix", "O'zbek tili"],
        "mavzular": ["Daraja 1: Kirish", "Daraja 2: Asoslar", "Daraja 3: Murakkab"]
    }

# 3. AI Maslahatchi (Sun'iy intellekt - Kommentariyada)
# @app.post("/ask-ai")
# async def ask_ai(data: UserAction):
#     prompt = f"{data.fan} fani bo'yicha savol: {data.savol}"
#     response = model.generate_content(prompt)
#     return {"javob": response.text}

# 4. Ballar va Kitoblar (Gamification - Baza simulyatsiyasi bilan)
@app.post("/exchange")
async def exchange_points(data: UserAction):
    if data.ism in db_users:
        # Ballarni ayirish logikasi
        db_users[data.ism]["ball"] -= data.ball
        return {"message": f"{data.ball} ball evaziga elektron kitob berildi!"}
    return {"message": "Foydalanuvchi topilmadi"}