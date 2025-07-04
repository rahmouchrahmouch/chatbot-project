import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Pinecone as LangchainPinecone
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings

# 📦 Variables d'environnement
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

# 🔍 Embeddings
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 🧠 LLMs spécialisés
llm_coach = ChatOpenAI(
    openai_api_key=GROQ_API_KEY,
    openai_api_base="https://api.groq.com/openai/v1",
    model_name="llama3-8b-8192",
    temperature=0.7
)

llm_legal = ChatOpenAI(
    openai_api_key=GROQ_API_KEY,
    openai_api_base="https://api.groq.com/openai/v1",
    model_name="llama3-8b-8192",
    temperature=0.3
)

llm_default = ChatOpenAI(
    openai_api_key=GROQ_API_KEY,
    openai_api_base="https://api.groq.com/openai/v1",
    model_name="llama3-8b-8192",
    temperature=0.5
)

# 🧠 Vectorstores (même index ici, mais extensible)
vectorstore_coach = LangchainPinecone.from_existing_index(
    index_name=PINECONE_INDEX_NAME,
    embedding=embedding_model,
    text_key="page_content"
)

vectorstore_legal = LangchainPinecone.from_existing_index(
    index_name=PINECONE_INDEX_NAME,
    embedding=embedding_model,
    text_key="page_content"
)

vectorstore_default = LangchainPinecone.from_existing_index(
    index_name=PINECONE_INDEX_NAME,
    embedding=embedding_model,
    text_key="page_content"
)

# 🎯 Fonction principale
def ask_question(query: str, user_id: str, role: str) -> dict:
    print(f"📨 Requête de [{user_id}] avec rôle [{role}]")

    # 🔀 Sélection dynamique selon le rôle
    if role == "coach":
        llm = llm_coach
        vectorstore = vectorstore_coach
        prefix = "[Coach] "
    elif role == "legal_advisor":
        llm = llm_legal
        vectorstore = vectorstore_legal
        prefix = "[Conseiller juridique] "
    else:
        llm = llm_default
        vectorstore = vectorstore_default
        prefix = ""

    full_query = prefix + query
    retriever = vectorstore.as_retriever(search_kwargs={"include_metadata": True, "include_values": True})
    try:
     results = retriever.get_relevant_documents(full_query)
    except Exception as e:
      print("❌ Erreur lors de l'appel à retriever.invoke():", e)
      raise  # Pour que FastAPI affiche aussi une trace complète



    score_threshold = 0.3
    relevant_chunks = [doc for doc in results if doc.metadata.get("score", 0) >= score_threshold]

    if not relevant_chunks:
        return {
            "query": full_query,
            "result": "❌ Aucun document pertinent trouvé pour cette requête.",
            "sources": [],
            "context": []
        }

    # 📄 Extraire les sources et contextes
    sources = list({doc.metadata.get("source", "inconnu") for doc in relevant_chunks[:3]})
    context_chunks = [doc.page_content for doc in relevant_chunks[:3]]

    # 💬 Génération via LLM
    rag_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())
    response = rag_chain.invoke({"query": full_query})

    return {
        "query": full_query,
        "result": response['result'] if isinstance(response, dict) else response,
        "sources": sources,
        "context": context_chunks
    }