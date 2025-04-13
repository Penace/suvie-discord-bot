import React, { useState } from 'react'
import ChatBubble from '../components/ChatBubble'

export default function Ai() {
  const [messages, setMessages] = useState([
    { sender: 'suvie', text: "Hey there! I'm Suvie — your media companion. Ask me anything!" }
  ])
  const [input, setInput] = useState("")

  const handleSend = () => {
    if (!input.trim()) return

    const userMsg = { sender: 'user', text: input.trim() }
    const aiResponse = {
      sender: 'suvie',
      text: "That's interesting! I'm still learning — try again once I'm fully online 🧠"
    }

    setMessages(prev => [...prev, userMsg])
    setInput("")

    setTimeout(() => {
      setMessages(prev => [...prev, aiResponse])
    }, 500)
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') handleSend()
  }

  return (
    <div className="flex flex-col h-[calc(100vh-80px)]">
      <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-black">
        {messages.map((msg, i) => (
          <ChatBubble key={i} message={msg} />
        ))}
      </div>
      <div className="bg-zinc-900 border-t border-zinc-800 p-4 flex items-center gap-2">
        <input
          type="text"
          value={input}
          placeholder="Ask Suvie something..."
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyPress}
          className="flex-1 bg-zinc-800 rounded px-4 py-2 text-white focus:outline-none"
        />
        <button
          onClick={handleSend}
          className="bg-pink-500 hover:bg-pink-600 text-white px-4 py-2 rounded transition"
        >
          Send
        </button>
      </div>
    </div>
  )
}
