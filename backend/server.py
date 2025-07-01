from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Autoriser les requêtes depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # autorise tout domaine, à restreindre ensuite si besoin
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    user_message = req.message
    # Simule une réponse pour le moment
    return {"response": f"Tu as dit : {user_message}. (réponse simulée)"}
