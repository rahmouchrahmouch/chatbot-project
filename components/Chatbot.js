// Chatbot.js
import React, { useState } from "react";
import axios from "axios";

function Chatbot() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMessage = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const res = await axios.post("http://127.0.0.1:5000/chat", {
        message: input,
      });
      const botMessage = { sender: "bot", text: res.data.response };
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      console.error(err);
    }
    setInput("");
  };

  return (
    <div style={{ maxWidth: "600px", margin: "auto" }}>
      <h2>Chatbot IA Générative</h2>
      <div style={{ border: "1px solid #ccc", padding: 10, height: 300, overflowY: "scroll" }}>
        {messages.map((msg, i) => (
          <div key={i} style={{ textAlign: msg.sender === "user" ? "right" : "left" }}>
            <b>{msg.sender === "user" ? "Vous" : "Bot"}:</b> {msg.text}
          </div>
        ))}
      </div>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Posez une question..."
        style={{ width: "80%" }}
      />
      <button onClick={sendMessage}>Envoyer</button>
    </div>
  );
}

export default Chatbot;
