"use client";

import { useState, useRef, useEffect } from "react";
import { BotIcon, UserIcon } from "lucide-react";
import { v4 as uuidv4 } from "uuid";

type Message = {
  author: "user" | "bot";
  text: string;
  sources?: string[];
};

const ROLES = [
  { value: "coach", label: "Coach" },
  { value: "legal_advisor", label: "Conseiller juridique" },
  { value: "default", label: "Utilisateur" },
];

export default function ChatBox() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [chatHistory, setChatHistory] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [userId, setUserId] = useState<string | null>(null);
  const [userRole, setUserRole] = useState<string>("default");
  const [showHistory, setShowHistory] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Init userId et userRole + charger historique
  useEffect(() => {
    let storedId = localStorage.getItem("userId");
    if (!storedId) {
      storedId = uuidv4();
      localStorage.setItem("userId", storedId);
    }
    setUserId(storedId);

    const storedRole = localStorage.getItem("userRole") || "default";
    setUserRole(storedRole);

    const historyKey = `chatHistory_${storedId}`;
    const storedHistory = JSON.parse(localStorage.getItem(historyKey) || "[]");
    setChatHistory(storedHistory);
    setMessages(storedHistory);
  }, []);

  // Sauvegarder userRole dans localStorage à chaque changement
  useEffect(() => {
    localStorage.setItem("userRole", userRole);
  }, [userRole]);

  // Scroll auto vers bas à chaque nouveau message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Sauvegarder l’historique complet dans localStorage par userId
  const saveChatHistory = (newHistory: Message[]) => {
    if (!userId) return;
    const historyKey = `chatHistory_${userId}`;
    localStorage.setItem(historyKey, JSON.stringify(newHistory));
  };

  // Ajouter message à l’historique et sauvegarder
  const addMessageToHistory = (newMessage: Message) => {
    setChatHistory((prev) => {
      const updated = [...prev, newMessage];
      saveChatHistory(updated);
      return updated;
    });
  };

  // Envoyer message au backend
  const sendMessage = async (text: string) => {
    if (!text.trim() || !userId) return;

    const userMsg: Message = { author: "user", text };
    setMessages((msgs) => [...msgs, userMsg]);
    addMessageToHistory(userMsg);
    setInput("");
    setIsTyping(true);

    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text, userId, role: userRole }),
      });

      const data = await res.json();
      const botMsg: Message = {
        author: "bot",
        text: data.response,
        sources: data.sources,
      };
      setMessages((msgs) => [...msgs, botMsg]);
      addMessageToHistory(botMsg);
    } catch {
      const errMsg: Message = {
        author: "bot",
        text: "Erreur serveur. Veuillez réessayer.",
      };
      setMessages((msgs) => [...msgs, errMsg]);
      addMessageToHistory(errMsg);
    } finally {
      setIsTyping(false);
    }
  };

  // Gérer clic sur “Envoyer”
  const handleSend = () => sendMessage(input);

  // Envoi avec Enter (sans Shift)
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto mt-10 p-6 bg-white dark:bg-gray-900 rounded-2xl shadow-xl flex flex-col h-[750px] border border-gray-300 dark:border-gray-700">
      {/* Choix du rôle */}
      <div className="mb-4">
        <label
          htmlFor="role-select"
          className="block mb-1 font-semibold text-gray-700 dark:text-gray-300"
        >
          Choisissez votre rôle :
        </label>
        <select
          id="role-select"
          value={userRole}
          onChange={(e) => setUserRole(e.target.value)}
          className="p-2 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
        >
          {ROLES.map(({ value, label }) => (
            <option key={value} value={value}>
              {label}
            </option>
          ))}
        </select>
      </div>

      {/* Bouton pour afficher/cacher l'historique */}
      <div className="mb-4">
        <button
          onClick={() => setShowHistory(!showHistory)}
          className="bg-gray-300 dark:bg-gray-700 px-4 py-2 rounded hover:bg-gray-400 dark:hover:bg-gray-600"
        >
          {showHistory ? "Cacher l'historique" : "Voir l'historique"}
        </button>
      </div>

      {/* Affichage de l'historique complet */}
      {showHistory && (
        <div className="mb-6 max-h-60 overflow-y-auto border border-gray-400 rounded p-3 bg-gray-50 dark:bg-gray-800">
          {chatHistory.length === 0 && (
            <p className="text-sm italic">Aucun historique.</p>
          )}
          {chatHistory.map((msg, idx) => (
            <div
              key={idx}
              className={`mb-1 ${
                msg.author === "user"
                  ? "text-right text-blue-600"
                  : "text-left text-gray-800 dark:text-gray-200"
              }`}
            >
              <strong>{msg.author === "user" ? "Vous:" : "Assistant:"}</strong>{" "}
              {msg.text}
              {msg.author === "bot" && msg.sources && msg.sources.length > 0 && (
                <div className="text-xs text-blue-400">
                  Source(s): {msg.sources.join(", ")}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Zone de chat principale */}
      <div className="flex-1 overflow-y-auto space-y-4 pr-2">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex ${
              msg.author === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div className="flex items-start gap-2 max-w-[80%]">
              {msg.author === "bot" && (
                <div className="p-1 bg-gray-300 dark:bg-gray-700 rounded-full">
                  <BotIcon className="w-5 h-5 text-gray-800 dark:text-gray-200" />
                </div>
              )}
              <div
                className={`rounded-xl px-4 py-2 text-sm ${
                  msg.author === "user"
                    ? "bg-blue-600 text-white rounded-br-none"
                    : "bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-100 rounded-bl-none"
                }`}
              >
                <div>{msg.text}</div>
                {msg.author === "bot" && msg.sources && msg.sources.length > 0 && (
                  <div className="text-xs mt-2 text-blue-400">
                    Source(s): {msg.sources.join(", ")}
                  </div>
                )}
              </div>
              {msg.author === "user" && (
                <div className="p-1 bg-blue-600 rounded-full">
                  <UserIcon className="w-5 h-5 text-white" />
                </div>
              )}
            </div>
          </div>
        ))}

        {isTyping && (
          <div className="flex items-center gap-2 text-sm italic text-gray-500 dark:text-gray-400 animate-pulse">
            <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-75"></span>
            <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-150"></span>
            <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-300"></span>
            <span>L&apos;assistant écrit...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input + bouton */}
      <div className="mt-4 flex gap-2">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          rows={1}
          className="flex-1 resize-none rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Écris ton message..."
        />
        <button
  onClick={handleSend}
  disabled={!input.trim()}
  className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-xl transition disabled:bg-blue-300"
>
  Envoyer
</button>

      </div>
    </div>
  );
}
