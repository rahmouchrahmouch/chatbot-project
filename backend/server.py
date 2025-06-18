from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from fastapi.middleware.cors import CORSMiddleware
import os

# Initialiser FastAPI
app = FastAPI()

# Permettre les requêtes CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèle pour la requête
class QuestionRequest(BaseModel):
    question: str

# Charger et configurer les documents et le vectorstore
def load_vectorstore():
    pdf_path = "Tendances_Mode_2025.pdf"  # Assurez-vous que ce fichier existe dans votre dossier
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Le fichier {pdf_path} n'existe pas.")

    loader = PyPDFLoader(pdf_path)
    pages = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""]
    )
    docs = text_splitter.split_documents(pages)

    embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embedding_function)
    return vectorstore

# Charger le vectorstore
vectorstore = load_vectorstore()

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur le serveur du chatbot!"}

@app.post("/chat")
async def chat(question_request: QuestionRequest):
    question = question_request.question
    # Utiliser LangChain pour récupérer et générer une réponse
    # Exemple simplifié
    docs = vectorstore.similarity_search(question)
    response_text = " ".join([doc.page_content for doc in docs])
    response = {"response": f"Réponse basée sur le document: {response_text}"}
    return response
