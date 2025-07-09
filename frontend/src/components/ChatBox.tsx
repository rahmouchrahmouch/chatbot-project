"use client";

import { useState, useEffect, useRef } from "react";
import { v4 as uuidv4 } from "uuid";
import ChatBubble from "./ChatBubble";
import TypingIndicator from "./TypingIndicator";
import ChatInput from "./ChatInput";
import { saveAs } from "file-saver";

// Type Message
type Message = {
  author: "user" | "bot";
  text: string;
  sources?: string[];
};

// Liste des modèles
const MODELS = [
  "llama-3.1-8b-instant",
  "llama-3.3-70b-versatile",
  "gemma2-9b-it",
  "mixtral-8x7b-32768",
  "qwen-qwq-32b",
  "mistral-saba-24b"
];

export default function ChatBox() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [chatHistory, setChatHistory] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [userId, setUserId] = useState<string | null>(null);
  const [showHistory, setShowHistory] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [selectedModel, setSelectedModel] = useState(MODELS[0]);
  const [requestCount, setRequestCount] = useState<number>(0); // compteur local

  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (typeof window === "undefined") return;
    let storedId = localStorage.getItem("userId");
    if (!storedId) {
      storedId = uuidv4();
      localStorage.setItem("userId", storedId);
    }
    setUserId(storedId);

    // Charger historique
    const historyKey = `chatHistory_${storedId}`;
    try {
      const storedHistory = JSON.parse(localStorage.getItem(historyKey) || "[]");
      setChatHistory(storedHistory);
      setMessages(storedHistory);
    } catch (err) {
      console.error("Erreur de chargement historique :", err);
    }

    // Charger compteur depuis localStorage
    const savedCount = localStorage.getItem("requestCount");
    if (savedCount) setRequestCount(parseInt(savedCount, 10));
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    // Sauvegarder compteur dans localStorage
    localStorage.setItem("requestCount", requestCount.toString());
  }, [requestCount]);

  const saveChatHistory = (newHistory: Message[]) => {
    if (!userId) return;
    localStorage.setItem(`chatHistory_${userId}`, JSON.stringify(newHistory));
  };

  const addMessageToHistory = (msg: Message) => {
    setChatHistory((prev) => {
      const updated = [...prev, msg];
      saveChatHistory(updated);
      return updated;
    });
  };

  const clearHistory = () => {
    if (!userId) return;
    localStorage.removeItem(`chatHistory_${userId}`);
    setChatHistory([]);
    setMessages([]);
  };

  const downloadHistory = () => {
    const blob = new Blob([JSON.stringify(chatHistory, null, 2)], { type: "application/json" });
    saveAs(blob, "chat_history.json");
  };

  const sendMessage = async (text: string) => {
    if (!text.trim() || !userId) return;
    const userMsg: Message = { author: "user", text };
    setMessages((prev) => [...prev, userMsg]);
    addMessageToHistory(userMsg);
    setInput("");
    setIsTyping(true);

    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text, userId, model: selectedModel }),
      });

      if (!res.ok) throw new Error("Erreur serveur");

      const data = await res.json();

      // Incrémenter compteur local à chaque requête réussie
      setRequestCount((prev) => prev + 1);

      const botMsg: Message = {
        author: "bot",
        text: data.response,
        sources: data.sources,
      };
      setMessages((prev) => [...prev, botMsg]);
      addMessageToHistory(botMsg);
    } catch (err: any) {
      const errorMsg: Message = {
        author: "bot",
        text: `Erreur serveur : ${err.message || "réessayez plus tard"}`,
      };
      setMessages((prev) => [...prev, errorMsg]);
      addMessageToHistory(errorMsg);
    } finally {
      setIsTyping(false);
    }
  };

  const handleSend = () => sendMessage(input);
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto mt-10 p-6 bg-white dark:bg-gray-900 rounded-2xl shadow-xl flex flex-col h-[750px] border border-gray-300 dark:border-gray-700">
      
      {/* Menu déroulant à 3 traits */}
      <div className="flex items-center justify-between mb-4 gap-4">
        <div className="relative">
          <button
            onClick={() => setMenuOpen(!menuOpen)}
            className="text-gray-700 bg-gray-200 px-3 py-2 rounded hover:bg-gray-300 dark:text-white dark:bg-gray-700"
          >
            &#9776; {/* Icône ≡ */}
          </button>
          {menuOpen && (
            <div className="absolute mt-2 w-48 rounded shadow bg-white dark:bg-gray-800 text-sm z-50">
              <button
                onClick={() => setShowHistory((prev) => !prev)}
                className="block w-full px-4 py-2 text-left hover:bg-gray-100 dark:hover:bg-gray-700"
              >
                {showHistory ? "Cacher l’historique" : "Voir l’historique"}
              </button>
              <button
                onClick={clearHistory}
                className="block w-full px-4 py-2 text-left hover:bg-gray-100 dark:hover:bg-gray-700"
              >
                Effacer l’historique
              </button>
              <button
                onClick={downloadHistory}
                className="block w-full px-4 py-2 text-left hover:bg-gray-100 dark:hover:bg-gray-700"
              >
                Télécharger
              </button>
            </div>
          )}
        </div>

        {/* Sélecteur de modèle */}
        <div>
          <select
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value)}
            className="border border-gray-400 rounded px-3 py-2 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
          >
            {MODELS.map((model) => (
              <option key={model} value={model}>
                {model}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Affichage historique si activé */}
      {showHistory && (
        <div className="mb-6 max-h-60 overflow-y-auto border border-gray-400 rounded p-3 bg-gray-50 dark:bg-gray-800">
          {chatHistory.length === 0 ? (
            <p className="text-sm italic">Aucun historique.</p>
          ) : (
            chatHistory.map((msg, idx) => <ChatBubble key={idx} {...msg} />)
          )}
        </div>
      )}

      {/* Affichage des messages */}
      <div className="flex-1 overflow-y-auto space-y-4 pr-2">
        {messages.map((msg, idx) => (
          <ChatBubble key={idx} {...msg} />
        ))}
        {isTyping && <TypingIndicator />}
        <div ref={messagesEndRef} />
      </div>

      {/* Affichage compteur requêtes */}
      <div className="text-sm text-gray-500 dark:text-gray-400 mt-2 text-center">
        Nombre de requêtes effectuées : {requestCount}
      </div>

      {/* Entrée utilisateur */}
      <ChatInput
        input={input}
        setInput={setInput}
        handleSend={handleSend}
        handleKeyDown={handleKeyDown}
      />
    </div>
  );
}
