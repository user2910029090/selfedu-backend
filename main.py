from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SelfEdu_Ai API")

# Frontend bilan muammosiz ulanishi uchun sozlama
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Qabul qilinadigan ma'lumotlar qolipi
class UserLogin(BaseModel):
    ism: str
    familiya: str

class AIChat(BaseModel):
    fan_nomi: str
    savol: str

# 1. Kirish qismi
@app.post("/login")
async def login(user: UserLogin):
    return {
        "status": "muvaffaqiyatli",
        "xabar": f"Xush kelibsiz, {user.ism} {user.familiya}!"
    }

# 2. AI yordamchi qismi (Hozircha oddiy javob qaytaradi)
@app.post("/chat")
async def chat_with_ai(data: AIChat):
    javob = f"Siz {data.fan_nomi} fani bo'yicha savol berdingiz: '{data.savol}'. AI ulanishi jarayonda!"
    return {
        "fan": data.fan_nomi,
        "ai_javobi": javob
    }

# Dasturni ishga tushirish
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)