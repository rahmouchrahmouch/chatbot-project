from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_pipeline import ask_question

# Initialisation de l'application FastAPI
app = FastAPI()

# 🔓 Autoriser les requêtes CORS depuis ton frontend (localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📬 Modèle de la requête attendue
class ChatRequest(BaseModel):
    message: str

# 📤 Modèle de la réponse
class ChatResponse(BaseModel):
    response: str

# 📩 Endpoint POST /chat
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    user_msg = req.message

   # Appel réel à la chaîne RAG
    response = ask_question(user_msg)

    return {"response": response}
