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

# Charger les variables d’environnement
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")  # ex: "us-west-2"
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

DOCS_FOLDER = "C:/Users/rahma/Downloads/chatbot-project/data/docs"

# Initialisation Pinecone (nouveau SDK)
pc = Pinecone(api_key=PINECONE_API_KEY)

# Créer l'index s'il n'existe pas
if PINECONE_INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region=PINECONE_ENVIRONMENT)
    )

# Connexion à l'index Pinecone
index = pc.Index(PINECONE_INDEX_NAME)

# Fonction pour charger les documents
def load_documents(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        ext = filename.lower().split('.')[-1]

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
            else:
                print(f"⚠️ Format non supporté : {filename}")
                continue

            docs = loader.load()
            documents.extend(docs)
            print(f"📄 Chargé : {filename}")
        except Exception as e:
            print(f"❌ Erreur avec {filename} : {e}")
    return documents

# Fonction pour découper les documents
def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.split_documents(documents)

# Fonction principale
def main():
    docs = load_documents(DOCS_FOLDER)
    print(f"📄 Total documents chargés : {len(docs)}")

    docs_split = split_documents(docs)
    print(f"🧩 Documents après découpage : {len(docs_split)}")

    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    LangchainPinecone.from_documents(
        documents=docs_split,
        embedding=embedding,
        index_name=PINECONE_INDEX_NAME,
        text_key="page_content"
    )
    print("✅ Ingestion et indexation terminées.")

if __name__ == "__main__":
    main()
