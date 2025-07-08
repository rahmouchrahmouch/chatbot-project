import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Pinecone as LangchainPinecone
from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceEmbeddings

# 📦 Variables d'environnement
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

# 🔍 Embeddings
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 💬 Modèle LLM
llm = ChatOpenAI(
    openai_api_key=GROQ_API_KEY,
    openai_api_base="https://api.groq.com/openai/v1",
    model_name="llama3-8b-8192",
    temperature=0.5
)

# 🧠 Vectorstore
vectorstore = LangchainPinecone.from_existing_index(
    index_name=PINECONE_INDEX_NAME,
    embedding=embedding_model,
    text_key="page_content"
)

# 🎯 Fonction principale
def ask_question(query: str, user_id: str) -> dict:
    print(f"📨 Question de [{user_id}] : {query}")
    retriever = vectorstore.as_retriever()

    try:
        results = retriever.invoke(query)
    except Exception as e:
        print("❌ Erreur lors de la récupération :", e)
        raise

    if not results:
        return {
            "query": query,
            "result": "❌ Aucun document pertinent trouvé.",
            "sources": [],
            "context": []
        }

    # 📄 Extraction des sources et du contexte
    sources = list({doc.metadata.get("source", "inconnu") for doc in results[:3]})
    context_chunks = [doc.page_content for doc in results[:3]]

    # 💡 Génération de la réponse
    rag_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    response = rag_chain.invoke({"query": query})

    return {
        "query": query,
        "result": response['result'] if isinstance(response, dict) else response,
        "sources": sources,
        "context": context_chunks
    }