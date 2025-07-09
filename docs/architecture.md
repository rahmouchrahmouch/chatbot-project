# 🏗️ Architecture Technique du Chatbot IA Génératif

## 🧠 1. Objectif du Projet

Ce projet a pour but de concevoir un chatbot intelligent capable de répondre à des questions en langage naturel, tout en s’appuyant sur des documents techniques internes (via le RAG - Retrieval-Augmented Generation). L’IA peut donc combiner ses connaissances générales avec des données spécifiques fournies par l’utilisateur.

---

## 🏗️ 2. Architecture Générale

L'architecture est basée sur une structure **Full Stack** :

- **Frontend** : Next.js (React)
- **Backend** : FastAPI avec Uvicorn
- **Moteur IA** : LangChain + HuggingFace Embeddings
- **Base vectorielle** : Pinecone
- **Stockage local des fichiers** : `data/docs/`

---

## ⚙️ 3. Pipeline de Traitement (RAG)

### 📥 Étape 1 : Ingestion des documents
- Formats supportés : `.pdf`, `.docx`, `.txt`, `.md`, `.html`
- Utilisation de LangChain (`PyPDFLoader`, `TextLoader`, etc.)
- Les documents sont stockés dans `data/docs/`.

### ✂️ Étape 2 : Découpage (chunking)
- Découpage des documents en morceaux de 1000 caractères avec chevauchement de 200 (`RecursiveCharacterTextSplitter`)

### 🧠 Étape 3 : Embedding
- Modèle utilisé : `sentence-transformers/all-MiniLM-L6-v2` via `HuggingFaceEmbeddings`
- Chaque chunk est transformé en vecteur.

### 🗃️ Étape 4 : Indexation dans Pinecone
- Pinecone est utilisé comme base de données vectorielle.
- Index dynamique créé si non existant.

### ❓ Étape 5 : Question/Réponse
- L’utilisateur pose une question via l’interface.
- Le backend utilise `retriever.invoke()` pour retrouver les chunks les plus pertinents.
- Une réponse est générée par l’IA à partir de la question + documents retrouvés.

---

## 🖥️ 4. Frontend (Next.js)

- Interface utilisateur avec React
- Composants : `ChatBox`, `ChatBubble`, `ChatToolbar`, `ChatInput`, `TypingIndicator`
- Historique des conversations sauvegardé dans `localStorage`
- Affichage des sources si disponibles

---

## 🧪 5. Backend (FastAPI)

- Route principale : `POST /chat`
- Analyse de la requête utilisateur, récupération des documents, génération de réponse
- Appels aux modules LangChain, embeddings, Pinecone

---

## 🔐 6. Sécurité & Confidentialité

- Aucune donnée sensible n’est stockée sur un serveur
- Les documents sont locaux ou hébergés temporairement pour indexation
- Pinecone est configuré avec des clés API sécurisées via `.env`

---

## 📂 7. Répertoires Clés

chatbot-project/
│
├── backend/
│ ├── rag_pipeline.py # pipeline RAG principal
│ ├── server.py # API FastAPI
│ ├── ingest_documents.py # ingestion des documents
│
├── frontend/
│ └── src/components/ # Chat UI
│
├── data/docs/ # documents à ingérer (PDF, Word, etc.)
├── .env # clés API Pinecone, etc.
└── docs/architecture.md # cette documentation technique
└── docs/guid_utilisateur.md


---

## 🏁 8. Limites et Améliorations Futures

- L’IA ne connaît que les documents fournis (pas d’accès internet).
- Possibilité d’ajouter l’upload dynamique de fichiers par l’utilisateur.
- Intégration future possible de modèles plus puissants (OpenAI, Mistral, Claude...).

## 9. Schéma 
Utilisateur (Next.js)
       |
       v
Question → Frontend → API FastAPI (/chat)
                         |
                         v
       [RAG Pipeline - LangChain]
            ├── Retriever (Pinecone)
            ├── LLM (ChatOpenAI / HuggingFace)
            └── Génération réponse
                         |
                         v
                 Réponse + Sources
                         |
                         v
                   Frontend (UI)

