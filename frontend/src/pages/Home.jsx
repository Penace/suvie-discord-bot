import React, { useEffect, useRef, useState } from "react";
import ChatBubble from "../components/ChatBubble";
import { Link } from "react-router-dom";

export default function Home() {
  const [showChat, setShowChat] = useState(false);
  const [messages, setMessages] = useState([
    {
      sender: "suvie",
      text: "Hey! I'm suvie. Ask me anything about your watchlist 👀",
    },
  ]);
  const [input, setInput] = useState("");
  const chatRef = useRef(null);

  const features = [
    {
      icon: "🎬",
      title: "Smart Watchlists",
      desc: "Track movies & shows with season/episode detail.",
    },
    {
      icon: "📥",
      title: "Downloaded List",
      desc: "Store filepaths for downloaded media.",
    },
    {
      icon: "✅",
      title: "Watched Archive",
      desc: "Log what you’ve watched and keep your history.",
    },
    {
      icon: "🤖",
      title: "suvie AI Assistant",
      desc: "Chat with an OpenAI-powered media companion.",
    },
    {
      icon: "🔁",
      title: "Dynamic Reloads",
      desc: "Update commands and features without restarts.",
    },
    {
      icon: "📊",
      title: "Status & Insights",
      desc: "System info, active media count, and more.",
    },
  ];

  const handleSend = () => {
    if (!input.trim()) return;
    const userMsg = { sender: "user", text: input.trim() };
    const suvieReply = {
      sender: "suvie",
      text: "That's interesting! I'm still learning — ask again when I'm fully online 🔧",
    };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setTimeout(() => setMessages((prev) => [...prev, suvieReply]), 600);
  };

  const handleKey = (e) => {
    if (e.key === "Enter") handleSend();
  };

  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="text-center mt-16 space-y-12 relative">
      <div className="space-y-6">
        <h1 className="text-5xl font-bold text-pink-400 animate-pulse">
          🎬 suvie
        </h1>
        <p className="text-lg text-gray-300 max-w-xl mx-auto">
          Your personal movie & TV companion — manage your watchlist, track
          downloads, and log everything you watch.
        </p>
        <div className="flex flex-wrap justify-center gap-4">
          <a
            href="/watchlist"
            className="bg-pink-500 hover:bg-pink-600 text-white font-bold py-2 px-6 rounded-xl transition"
          >
            Launch App
          </a>
          <a
            href="/docs"
            className="bg-gray-800 hover:bg-gray-700 text-white font-bold py-2 px-6 rounded-xl transition"
          >
            View Docs
          </a>
          <button
            onClick={() => setShowChat(!showChat)}
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-xl transition"
          >
            💬 Chat with suvie
          </button>
          <Link
            to="/ai"
            className="bg-zinc-800 hover:bg-zinc-700 text-white font-bold py-2 px-6 rounded-xl transition"
          >
            Full AI Page →
          </Link>
        </div>
      </div>

      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 px-6 max-w-6xl mx-auto">
        {features.map((f, i) => (
          <div
            key={i}
            className="bg-zinc-900 border border-zinc-700 p-6 rounded-2xl shadow hover:shadow-lg transition text-left"
          >
            <h3 className="text-xl font-semibold text-white">
              {f.icon} {f.title}
            </h3>
            <p className="text-sm text-gray-400 mt-2">{f.desc}</p>
          </div>
        ))}
      </div>

      {/* Floating Chat Assistant */}
      <div
        className={`fixed bottom-6 right-6 max-w-md w-full transition-transform duration-300 z-50 ${
          showChat
            ? "translate-y-0 opacity-100"
            : "translate-y-10 opacity-0 pointer-events-none"
        }`}
      >
        <div className="bg-zinc-900 border border-zinc-700 rounded-xl overflow-hidden shadow-xl flex flex-col h-[400px]">
          <div
            ref={chatRef}
            className="flex-1 overflow-y-auto p-4 space-y-3 bg-black"
          >
            {messages.map((m, i) => (
              <div
                key={i}
                className={`transition-all duration-500 ${
                  m.sender === "suvie"
                    ? "animate-fade-in-left"
                    : "animate-fade-in-right"
                }`}
              >
                <ChatBubble message={m} />
              </div>
            ))}
          </div>
          <div className="flex p-4 border-t border-zinc-700 bg-zinc-900">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKey}
              placeholder="Ask suvie something..."
              className="flex-1 rounded-l bg-zinc-800 px-4 py-2 text-white focus:outline-none"
            />
            <button
              onClick={handleSend}
              className="bg-pink-500 hover:bg-pink-600 text-white px-4 py-2 rounded-r transition"
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
