"use client";

import { useState, useRef, useEffect } from "react";

type Message = {
  author: "user" | "bot";
  text: string;
};

export default function ChatBox() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll automatique vers le dernier message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Simuler réponse bot après envoi utilisateur
  const sendMessage = (text: string) => {
    if (!text.trim()) return;
    const userMsg = { author: "user", text };
    setMessages((msgs) => [...msgs, userMsg]);
    setInput("");
    setIsTyping(true);

    // Simuler délai réponse IA
    setTimeout(() => {
      const botMsg = {
        author: "bot",
        text: "Merci pour votre message. Ceci est une réponse simulée.",
      };
      setMessages((msgs) => [...msgs, botMsg]);
      setIsTyping(false);
    }, 1500);
  };

  // Envoi via bouton ou Enter
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
    <div className="max-w-xl mx-auto mt-10 p-6 border rounded-3xl shadow-lg bg-white dark:bg-gray-800 flex flex-col h-[500px]">
      <div className="flex-1 overflow-y-auto mb-4 space-y-3 px-2">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`max-w-[75%] p-3 rounded-xl break-words ${
              msg.author === "user"
                ? "bg-blue-500 text-white self-end rounded-br-none"
                : "bg-gray-200 text-gray-800 dark:bg-gray-700 dark:text-gray-200 self-start rounded-bl-none"
            }`}
          >
            {msg.text}
          </div>
        ))}
        {isTyping && (
          <div className="text-gray-500 italic self-start">Le bot écrit...</div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="flex gap-3">
        <textarea
          rows={1}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          className="flex-1 resize-none border border-gray-300 rounded-xl p-3 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
          placeholder="Tapez votre message ici..."
        />
        <button
          onClick={handleSend}
          disabled={!input.trim()}
          className="bg-blue-600 disabled:bg-blue-300 text-white font-semibold px-6 rounded-xl hover:bg-blue-700 transition"
          aria-label="Envoyer le message"
        >
          Envoyer
        </button>
      </div>
    </div>
  );
}
