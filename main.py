import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai
from prompt_engine import build_prompt

load_dotenv('.env')

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
print('GEMINI_API_KEY loaded:', GEMINI_API_KEY)

genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    name: str
    type: str
    traits: str
    message: str

@app.get("/models")
async def list_models():
    try:
        models = genai.list_models()
        return {"models": [model.name for model in models]}
    except Exception as e:
        return {"error": str(e)}

@app.post("/generate")
async def generate_dialogue(req: GenerateRequest):
    try:
        prompt = build_prompt(req.name, req.type, req.traits, req.message)
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        response = model.generate_content(prompt)
        reply = response.text.strip() if hasattr(response, 'text') else str(response)
        return {"npc": req.name, "reply": reply}
    except Exception as e:
        print("Error in /generate:", e)
        return {"error": str(e)}