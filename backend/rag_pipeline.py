import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_pinecone import Pinecone as LangchainPinecone
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings


# 📦 Charger les variables d'environnement
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

# 📚 Répertoire contenant les fichiers PDF
DOCS_DIRECTORY = "C:/Users/rahma/Downloads/chatbot-project/data/docs"

# 🤖 Modèle d'embedding
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")  # → dimension = 1024

# 🔨 Fonction : découper un document PDF
def load_and_split_documents(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(documents)

def index_documents(file_path):
    ext = file_path.lower().split('.')[-1]
    if ext == "pdf":
        loader = PyPDFLoader(file_path)
    elif ext in ["docx", "doc"]:
        from langchain.document_loaders import UnstructuredWordDocumentLoader
        loader = UnstructuredWordDocumentLoader(file_path)
    elif ext == "txt":
        from langchain.document_loaders import TextLoader
        loader = TextLoader(file_path)
    elif ext == "html":
        from langchain.document_loaders import UnstructuredHTMLLoader
        loader = UnstructuredHTMLLoader(file_path)
    elif ext == "md":
        from langchain.document_loaders import UnstructuredMarkdownLoader
        loader = UnstructuredMarkdownLoader(file_path)
    else:
        print(f"⚠️ Format non supporté : {file_path}")
        return

    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs_split = splitter.split_documents(documents)

    LangchainPinecone.from_documents(
        documents=docs_split,
        embedding=embedding_model,
        index_name=PINECONE_INDEX_NAME,
        text_key="page_content"
    )


# 🔁 Fonction : indexer tous les PDFs d'un dossier
def index_all_documents_in_directory(directory_path):
    supported_exts = {"pdf", "docx", "doc", "txt", "html", "md"}
    for filename in os.listdir(directory_path):
        if filename.lower().split('.')[-1] in supported_exts:
            file_path = os.path.join(directory_path, filename)
            print(f"📄 Indexation de : {filename}")
            index_documents(file_path)


# 🧩 Configurer LLM (Groq)
llm = ChatOpenAI(
    openai_api_key=GROQ_API_KEY,
    openai_api_base="https://api.groq.com/openai/v1",
    model_name="llama3-8b-8192"
)

# 🧮 Connecter l'index existant
vectorstore = LangchainPinecone.from_existing_index(
    index_name=PINECONE_INDEX_NAME,
    embedding=embedding_model,
    text_key="page_content"
)

# 🔗 Créer la chaîne RAG
rag_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())

# 🎯 Fonction d'interrogation
def ask_question(question: str) -> str:
    return rag_chain.invoke({"query": question})

# 🧪 Si lancé directement, indexer les PDF
if __name__ == "__main__":
    print("🚀 Indexation de tous les fichiers supportés dans le dossier docs...")
    index_all_documents_in_directory(DOCS_DIRECTORY)
    print("✅ Indexation terminée.")


    # Exemple de question
    print("🧠 Réponse à une question test :")
    response = ask_question("Quels sont les principes de base du management financier ?")
    print("🔍 Réponse :", response)