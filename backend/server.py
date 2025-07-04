from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
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

# ✅ Requête entrante avec champ role optionnel (défaut "default")
class ChatRequest(BaseModel):
    message: str
    userId: str  # pour identifier l'utilisateur
    role: Optional[str] = "default"  # nouveau champ role, optionnel

# ✅ Réponse sortante avec liste de sources
class ChatResponse(BaseModel):
    response: str
    sources: List[str]

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    user_msg = req.message
    user_id = req.userId
    user_role = req.role

    loop = asyncio.get_event_loop()

    try:
        # Passe le role en argument à ta fonction ask_question
        result = await loop.run_in_executor(executor, ask_question, user_msg, user_id, user_role)

        print("✅ Résultat brut reçu :", result)

        return {
            "response": result["result"],
            "sources": result["sources"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
