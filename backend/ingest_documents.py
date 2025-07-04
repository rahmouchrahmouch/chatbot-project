import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
    TextLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Pinecone as LangchainPinecone

# 🛠️ Chargement des variables d'environnement
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
DOCS_FOLDER = "C:/Users/rahma/Downloads/chatbot-project/data/docs"

# 🔌 Initialisation Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# 🔧 Création de l’index si nécessaire
if PINECONE_INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region=PINECONE_ENVIRONMENT)
    )

# 📡 Connexion à l'index
index = pc.Index(PINECONE_INDEX_NAME)

# 🔍 Fonction pour charger les documents d’un dossier
def load_documents(folder_path):
    documents = []
    supported_exts = {"pdf", "docx", "doc", "txt", "html", "md"}

    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        ext = filename.lower().split('.')[-1]

        if ext not in supported_exts:
            print(f"⚠️ Format non supporté : {filename}")
            continue

        try:
            if ext == "pdf":
                loader = PyPDFLoader(filepath)
            elif ext in ["docx", "doc"]:
                loader = UnstructuredWordDocumentLoader(filepath)
            elif ext == "txt":
                loader = TextLoader(filepath)
            elif ext == "html":
                loader = UnstructuredHTMLLoader(filepath)
            elif ext == "md":
                loader = UnstructuredMarkdownLoader(filepath)

            docs = loader.load()
            documents.extend(docs)
            print(f"📄 Document chargé : {filename} → {len(docs)} page(s)")
        except Exception as e:
            print(f"❌ Erreur avec {filename} : {e}")
    return documents

# ✂️ Fonction de découpage intelligent
def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.split_documents(documents)

# 🔁 Fonction principale d’ingestion
def main():
    print("📥 Démarrage de l'ingestion...")
    docs = load_documents(DOCS_FOLDER)
    print(f"📦 Total documents bruts : {len(docs)}")

    docs_split = split_documents(docs)
    print(f"🧩 Chunks extraits : {len(docs_split)}")

    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    LangchainPinecone.from_documents(
        documents=docs_split,
        embedding=embedding,
        index_name=PINECONE_INDEX_NAME,
        text_key="page_content"
    )

    print("✅ Ingestion terminée. Documents indexés avec succès.")

if __name__ == "__main__":
    main()