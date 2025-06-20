from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from fastapi.middleware.cors import CORSMiddleware
import os
import sys  # import sys en haut

# Initialiser FastAPI
app = FastAPI()

# Permettre les requêtes CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèle pour la requête
class QuestionRequest(BaseModel):
    question: str

# Charger et configurer les documents et le vectorstore
def load_vectorstore():
    pdf_path = r"C:\Users\rahma\Downloads\chatbot-project\data\pdfs\financial_management_basics.pdf"

    print("Test d'existence fichier:", os.path.exists(pdf_path))
    print("Chemin absolu:", os.path.abspath(pdf_path))
    print("Python version:", sys.version)

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
    docs = vectorstore.similarity_search(question)
    response_text = " ".join([doc.page_content for doc in docs])
    return {"response": f"Réponse basée sur le document: {response_text}"}
