import { useState } from "react";
import axios from "axios";

export default function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;
    
    setMessages([...messages, { role: "user", content: input }]);
    setInput("");
    setLoading(true);

    try {
      const response = await axios.post("http://localhost:5000/chat", { message: input });
      setMessages([...messages, { role: "user", content: input }, { role: "bot", content: response.data.response }]);
    } catch (error) {
      console.error("Error sending message", error);
    }
    setLoading(false);
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100 p-4">
      <div className="w-full max-w-md bg-white p-4 rounded-lg shadow-lg">
        <h1 className="text-xl font-bold mb-4 text-center">AI Medical Chatbot</h1>
        <div className="h-64 overflow-y-auto border p-2 mb-4 bg-gray-50">
          {messages.map((msg, index) => (
            <div key={index} className={`mb-2 p-2 rounded ${msg.role === "user" ? "bg-blue-200" : "bg-gray-200"}`}>
              <strong>{msg.role === "user" ? "You" : "Bot"}:</strong> {msg.content}
            </div>
          ))}
        </div>
        <div className="flex">
          <input
            type="text"
            className="flex-1 p-2 border rounded-l"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
          />
          <button
            onClick={sendMessage}
            className="bg-blue-500 text-white p-2 rounded-r"
            disabled={loading}
          >
            {loading ? "..." : "Send"}
          </button>
        </div>
      </div>
    </div>
  );
}
