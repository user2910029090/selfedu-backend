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

# 2. Fanlar va Mavzular (Frontend uchun yangilangan 5 tadan mavzu bilan)
@app.get("/data")
async def get_data():
    return {
        "fanlar": {
            "Biologiya": ["Hujayra", "DNK tuzilishi", "Fotosintez", "Genetika", "Evolyutsiya"],
            "Tarix": ["Qadimgi dunyo", "Amir Temur davri", "Mustamlakachilik", "Mustaqillik", "Zamonaviy tarix"],
            "O'zbek tili": ["Imlo", "So'z turkumlari", "Sintaksis", "Uslubiyat", "Matn tahlili"]
        }
    }

# Foydalanuvchilar natijalarini saqlash uchun
results_db = {} 

@app.post("/submit_result")
async def submit_result(user_name: str, score: int, task_id: int):
    # Har bir foydalanuvchi uchun alohida natija saqlash
    results_db[user_name] = {"score": score, "task_id": task_id}
    return {"status": "Saqlandi"}

@app.get("/admin/stats")
async def get_stats():
    # Admin uchun barcha natijalarni qaytarish
    return results_db

# 3. AI Maslahatchi (Sun'iy intellekt - Kommentariyada)
# @app.post("/ask-ai")
# async def ask_ai(data: UserAction):
#     prompt = f"{data.fan} fani bo'yicha savol: {data.savol}"
#     response = model.generate_content(prompt)

# 4. Ballar va Kitoblar (Gamification - Baza simulyatsiyasi bilan)
@app.post("/exchange")
async def exchange_points(data: UserAction):
    if data.ism in db_users:
        # Ballarni ayirish logikasi
        db_users[data.ism]["ball"] -= data.ball
        return {"message": f"{data.ball} ball evaziga elektron kitob berildi!"}
    return {"message": "Foydalanuvchi topilmadi"}