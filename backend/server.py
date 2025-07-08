from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from rag_pipeline import ask_question
import asyncio
from concurrent.futures import ThreadPoolExecutor

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

executor = ThreadPoolExecutor(max_workers=3)

# 📨 Données entrantes
class ChatRequest(BaseModel):
    message: str
    userId: str

# 📦 Données sortantes
class ChatResponse(BaseModel):
    response: str
    sources: List[str]

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    user_msg = req.message
    user_id = req.userId

    loop = asyncio.get_event_loop()

    try:
        result = await loop.run_in_executor(executor, ask_question, user_msg, user_id)
        print("✅ Résultat brut reçu :", result)

        return {
            "response": result["result"],
            "sources": result["sources"]
        }

    except Exception as e:
        print("❌ Erreur serveur :", e)
        raise HTTPException(status_code=500, detail=str(e))