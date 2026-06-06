from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SelfEdu_Ai API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserLogin(BaseModel):
    ism: str
    familiya: str

class AIChat(BaseModel):
    fan_nomi: str
    savol: str

# YANGI QO'SHILGAN QISM: Asosiy sahifa
@app.get("/")
async def asosiy_sahifa():
    return {"xabar": "SelfEdu_AI serveri muvaffaqiyatli ishlamoqda 24/7!"}

@app.post("/login")
async def login(user: UserLogin):
    return {
        "status": "muvaffaqiyatli",
        "xabar": f"Xush kelibsiz, {user.ism} {user.familiya}!"
    }

@app.post("/chat")
async def chat_with_ai(data: AIChat):
    javob = f"Siz {data.fan_nomi} fani bo'yicha savol berdingiz: '{data.savol}'. AI ulanishi jarayonda!"
    return {
        "fan": data.fan_nomi,
        "ai_javobi": javob
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)