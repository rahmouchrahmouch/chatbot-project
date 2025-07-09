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

# Compteur global de requêtes
request_count = 0

# 📨 Données entrantes
class ChatRequest(BaseModel):
    message: str
    userId: str

# 📦 Données sortantes
class ChatResponse(BaseModel):
    response: str
    sources: List[str]
    request_count: int

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    global request_count
    request_count += 1

    user_msg = req.message
    user_id = req.userId

    loop = asyncio.get_event_loop()

    try:
        # Appel à ask_question avec 2 arguments (message, user_id)
        result = await loop.run_in_executor(
            executor, lambda: ask_question(user_msg, user_id)
        )

        print("✅ Résultat brut reçu :", result)

        return {
            "response": result["result"],
            "sources": result["sources"],
            "request_count": request_count
        }

    except Exception as e:
        print("❌ Erreur serveur :", e)
        raise HTTPException(status_code=500, detail=str(e))
