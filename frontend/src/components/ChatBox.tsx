"use client";

import { useState, useRef, useEffect } from "react";
import { BotIcon, UserIcon } from "lucide-react";

type Message = {
  author: "user" | "bot";
  text: string;
};

export default function ChatBox() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async (text: string) => {
    if (!text.trim()) return;
    const userMsg: Message = { author: "user", text };
    setMessages((msgs) => [...msgs, userMsg]);
    setInput("");
    setIsTyping(true);

    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text }),
      });

      const data = await res.json();
      const botMsg: Message = { author: "bot", text: data.response };
      setMessages((msgs) => [...msgs, botMsg]);
    } catch (err) {
      setMessages((msgs) => [
        ...msgs,
        { author: "bot", text: "Erreur serveur. Veuillez réessayer." },
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleSend = () => {
    sendMessage(input);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto mt-10 p-6 bg-white dark:bg-gray-900 rounded-2xl shadow-xl flex flex-col h-[600px] border border-gray-300 dark:border-gray-700">
      <div className="flex-1 overflow-y-auto space-y-4 pr-2">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.author === "user" ? "justify-end" : "justify-start"}`}>
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
                {msg.text}
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
            <span>L'assistant écrit...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

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
