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

# Chargement des variables d'environnement
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
DOCS_FOLDER = "C:/Users/rahma/Downloads/chatbot-project/data/docs"

# Init Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

def infer_domain(filename):
    fname = filename.lower()
    if any(kw in fname for kw in ["juridique", "assistant", "foad", "cours"]):
        return "droit"
    elif any(kw in fname for kw in ["finance", "financial", "budget", "investissement"]):
        return "finance"
    elif any(kw in fname for kw in ["sante", "psychosocial", "mental", "retablissement", "smps", "outil"]):
        return "sante"
    elif any(kw in fname for kw in ["coaching", "debriefing", "cycle", "manual"]):
        return "coaching"
    elif any(kw in fname for kw in ["pedagogique", "cpc", "conseiller", "maternelle", "programme"]):
        return "education"
    elif any(kw in fname for kw in ["owasp", "anssi", "cybersecurite", "top10"]):
        return "cybersecurite"
    elif any(kw in fname for kw in ["analyst", "data", "remote_work", "readme", "jax", "csv"]):
        return "tech"
    elif any(kw in fname for kw in ["joe_", "journal", "officiel"]):
        return "administratif"
    else:
        return "autre"

def load_documents(folder_path):
    documents = []
    supported_exts = {"pdf", "docx", "doc", "txt", "html", "md"}

    files = os.listdir(folder_path)
    print(f"📂 Fichiers trouvés dans {folder_path} : {files}")

    for filename in files:
        filepath = os.path.join(folder_path, filename)
        ext = filename.lower().split('.')[-1]

        if ext not in supported_exts:
            print(f"⚠️ Format non supporté : {filename}")
            continue

        print(f"📥 Chargement de {filename} ({ext})...")

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
            for doc in docs:
                doc.metadata["source"] = filename
                doc.metadata["domain"] = infer_domain(filename)
            documents.extend(docs)
            print(f"✅ {filename} chargé avec {len(docs)} page(s)")

        except Exception as e:
            print(f"❌ Erreur avec {filename} : {e}")

    print(f"📦 Total documents chargés : {len(documents)}")
    return documents

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(documents)
    print(f"🧩 Total chunks extraits : {len(chunks)}")
    print("🔍 Exemples de chunks avec sources et domaines :")
    for chunk in chunks[:5]:
        print(f"- Source: {chunk.metadata.get('source')}, Domain: {chunk.metadata.get('domain')}")
        print(f"  Extrait texte : {chunk.page_content[:100].replace(chr(10), ' ')}...\n")
    return chunks

def main():
    # Supprimer index s'il existe
    if PINECONE_INDEX_NAME in pc.list_indexes().names():
        print(f"🗑️ Suppression de l'index existant : {PINECONE_INDEX_NAME}")
        pc.delete_index(PINECONE_INDEX_NAME)

    # Créer index
    print(f"⚙️ Création de l'index : {PINECONE_INDEX_NAME}")
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region=PINECONE_ENVIRONMENT)
    )
    index = pc.Index(PINECONE_INDEX_NAME)

    # Charger documents
    documents = load_documents(DOCS_FOLDER)

    # Découper
    chunks = split_documents(documents)

    # Embeddings
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Indexer
    print("📤 Indexation des chunks dans Pinecone...")
    LangchainPinecone.from_documents(
        documents=chunks,
        embedding=embedding_model,
        index_name=PINECONE_INDEX_NAME,
        text_key="page_content"
    )

    # Test recherche simple
    retriever = LangchainPinecone.from_existing_index(
        index_name=PINECONE_INDEX_NAME,
        embedding=embedding_model,
        text_key="page_content"
    ).as_retriever()

    test_query = "Quel est le rôle d’un assistant juridique en droit pénal ?"
    print(f"\n🔎 Test recherche sur la question : '{test_query}'")
    relevant_docs = retriever.get_relevant_documents(test_query)
    for i, doc in enumerate(relevant_docs[:5]):
        print(f"Result {i+1} - Source: {doc.metadata.get('source')}")
        print(f"Text: {doc.page_content[:200].replace(chr(10), ' ')}...\n")

if __name__ == "__main__":
    main()
