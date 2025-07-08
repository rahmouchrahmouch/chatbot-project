"use client";

import { useState, useEffect, useRef } from "react";
import { v4 as uuidv4 } from "uuid";
import ChatBubble from "./ChatBubble";
import ChatToolbar from "./ChatToolbar"; 
import TypingIndicator from "./TypingIndicator";
import ChatInput from "./ChatInput";
type Message = {
  author: "user" | "bot";
  text: string;
  sources?: string[];
};

export default function ChatBox() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [chatHistory, setChatHistory] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [userId, setUserId] = useState<string | null>(null);
  const [showHistory, setShowHistory] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (typeof window === "undefined") return;
    let storedId = localStorage.getItem("userId");
    if (!storedId) {
      storedId = uuidv4();
      localStorage.setItem("userId", storedId);
    }
    setUserId(storedId);

    const historyKey = `chatHistory_${storedId}`;
    try {
      const storedHistory = JSON.parse(localStorage.getItem(historyKey) || "[]");
      setChatHistory(storedHistory);
      setMessages(storedHistory);
    } catch (err) {
      console.error("Erreur de chargement historique :", err);
    }
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

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
        body: JSON.stringify({ message: text, userId }),
      });

      if (!res.ok) throw new Error("Erreur serveur");

      const data = await res.json();
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
      <div className="mb-4">
        <button
          onClick={() => setShowHistory(!showHistory)}
          className="bg-gray-300 dark:bg-gray-700 px-4 py-2 rounded hover:bg-gray-400 dark:hover:bg-gray-600"
          aria-pressed={showHistory}
        >
          {showHistory ? "Cacher l'historique" : "Voir l'historique"}
        </button>
      </div>

      <ChatToolbar
        userId={userId}
        chatHistory={chatHistory}
        setMessages={setMessages}
        setChatHistory={setChatHistory}
      />

      {showHistory && (
        <div className="mb-6 max-h-60 overflow-y-auto border border-gray-400 rounded p-3 bg-gray-50 dark:bg-gray-800">
          {chatHistory.length === 0 ? (
            <p className="text-sm italic">Aucun historique.</p>
          ) : (
            chatHistory.map((msg, idx) => <ChatBubble key={idx} {...msg} />)
          )}
        </div>
      )}

      <div className="flex-1 overflow-y-auto space-y-4 pr-2">
        {messages.map((msg, idx) => (
          <ChatBubble key={idx} {...msg} />
        ))}
        {isTyping && <TypingIndicator />}
        <div ref={messagesEndRef} />
      </div>

      <ChatInput
        input={input}
        setInput={setInput}
        handleSend={handleSend}
        handleKeyDown={handleKeyDown}
      />
    </div>
  );
}