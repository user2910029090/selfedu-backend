from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from groq import Groq  # Groq kutubxonasini ulaymiz

app = FastAPI()

# CORS - Frontend bilan xavfsiz bog'lanish uchun
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
# Server uyg'oq ekanini tekshirish uchun bosh sahifa yo'nalishi
@app.get("/")
async def root():
    return {"status": "alive", "message": "SelfEdu_Ai backend is working!"}
# Groq AI sozlamalari
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
ai_client = Groq(api_key=GROQ_API_KEY)

# Bazaviy simulyatsiya uchun xotira
db_users = {} 
results_db = {} 

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

# 2. Fanlar va Mavzular (5 tadan mavzu bilan)
@app.get("/data")
async def get_data():
    return {
        "fanlar": {
            "Biologiya": ["Hujayra", "DNK tuzilishi", "Fotosintez", "Genetika", "Evolyutsiya"],
            "Tarix": ["Qadimgi dunyo", "Amir Temur davri", "Mustamlakachilik", "Mustaqillik", "Zamonaviy tarix"],
            "O'zbek tili": ["Imlo", "So'z turkumlari", "Sintaksis", "Uslubiyat", "Matn tahlili"]
        }
    }

# 3. AI Maslahatchi (Groq LLaMA 3.1 modeli faollashtirildi)
@app.post("/ask-ai")
async def ask_ai(data: UserAction):
    # AI uchun maxsus tizimli so'rov yozamiz
    prompt = f"Siz intellektual o'qituvchisiz. Talabaga {data.fan} fani bo'yicha tushunarli javob bering. Savol: {data.savol}"
    
    try:
        completion = ai_client.chat.completions.create(
            model="llama-3.1-70b-versatile",  # Murakkab mantiq va o'zbek tili uchun eng kuchli model
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        ai_javob = completion.choices[0].message.content
        return {"status": "ok", "javob": ai_javob}
        
    except Exception as e:
        return {"status": "error", "message": f"AI ulanishida xatolik: {str(e)}"}

# 4. Foydalanuvchilar natijalarini saqlash uchun API
@app.post("/submit_result")
async def submit_result(user_name: str, score: int, task_id: int):
    # Har bir foydalanuvchi uchun alohida natija saqlash
    results_db[user_name] = {"score": score, "task_id": task_id}
    return {"status": "Saqlandi"}

# 5. Admin uchun barcha natijalarni qaytarish API
@app.get("/admin/stats")
async def get_stats():
    return results_db

# 6. Ballar va Kitoblar (Gamification)
@app.post("/exchange")
async def exchange_points(data: UserAction):
    if data.ism in db_users:
        # Ballarni ayirish logikasi
        db_users[data.ism]["ball"] -= data.ball
        return {"message": f"{data.ball} ball evaziga elektron kitob berildi!"}
    return {"message": "Foydalanuvchi topilmadi"}