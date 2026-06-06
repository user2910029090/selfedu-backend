from fastapi import FastAPI
import google.generativeai as genai
import os

app = FastAPI()

# API kalitni yuklash
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

@app.post("/chat")
async def chat(data: dict):
    try:
        user_input = data.get("savol")
        response = model.generate_content(user_input)
        return {"javob": response.text}
    except Exception as e:
        return {"xato": str(e)}