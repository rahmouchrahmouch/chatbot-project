import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Pinecone as LangchainPinecone
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA

# Chargement variables d’environnement
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

# Embeddings (à garder cohérent avec ingestion)
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# LLM (ChatOpenAI)
llm = ChatOpenAI(
    openai_api_key=GROQ_API_KEY,
    openai_api_base="https://api.groq.com/openai/v1",
    model_name="llama3-8b-8192",
    temperature=0.5
)

# Connexion à l’index Pinecone existant (avec tous les docs)
vectorstore = LangchainPinecone.from_existing_index(
    index_name=PINECONE_INDEX_NAME,
    embedding=embedding_model,
    text_key="page_content"
)

# Fonction principale pour poser une question
def ask_question(query: str, user_id: str) -> dict:
    print(f"📨 Question de [{user_id}] : {query}")

    # Récupérer plusieurs documents proches sémantiquement
    retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
    relevant_docs = retriever.get_relevant_documents(query)

    if not relevant_docs:
        print("⚠️ Aucun document trouvé.")
        return {
            "query": query,
            "result": "Aucune information disponible.",
            "sources": [],
            "context": [],
        }

    # Affichage debug des sources récupérées
    print("📚 Sources des documents récupérés :")
    for doc in relevant_docs:
        print(f"- {doc.metadata.get('source', 'inconnu')}")

    # Créer la chaîne de QA avec le retriever
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    # Obtenir la réponse (le texte de la réponse)
    response = qa_chain.run(query)

    return {
        "query": query,
        "result": response,
        "sources": list({doc.metadata.get("source", "inconnu") for doc in relevant_docs}),
        "context": [doc.page_content for doc in relevant_docs],
    }

# Test local (optionnel)
if __name__ == "__main__":
    question = "Quels sont les principes de la cybersécurité ?"
    user = "test_user"
    answer = ask_question(question, user)
    print("\nRéponse :", answer["result"])
    print("Sources :", answer["sources"])