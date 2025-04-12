import React, { useState } from "react";
import { sendMessage } from "./api";

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;
    const userMsg = { from: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);
    const botReply = await sendMessage(input);
    setMessages((prev) => [...prev, { from: "bot", text: botReply }]);
    setInput("");
    setLoading(false);
  };

  return (
    <div className="max-w-2xl mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">🤖 Чат с нейросетью</h1>
      <div className="bg-white rounded-xl shadow-md p-4 space-y-2 min-h-[300px]">
        {messages.map((m, i) => (
          <div key={i} className={m.from === "user" ? "text-blue-600" : "text-green-600"}>
            <strong>{m.from === "user" ? "Вы" : "Бот"}:</strong> {m.text}
          </div>
        ))}
        {loading && <div className="text-gray-500 animate-pulse">Бот думает...</div>}
      </div>
      <div className="flex mt-4">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-grow p-2 border rounded-l-xl"
          placeholder="Введите сообщение..."
        />
        <button onClick={handleSend} className="bg-blue-500 text-white px-4 rounded-r-xl">
          Отправить
        </button>
      </div>
    </div>
  );
}