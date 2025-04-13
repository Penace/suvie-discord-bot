import React from "react";

export default function ChatBubble({ message }) {
  const isUser = message.sender === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} gap-2`}>
      {!isUser && <div className="text-2xl pt-1">🤖</div>}
      <div
        className={`
        max-w-[80%] sm:max-w-md px-4 py-2 rounded-xl shadow
        ${
          isUser
            ? "bg-pink-500 text-white rounded-br-none"
            : "bg-zinc-800 text-gray-100 rounded-bl-none"
        }
      `}
      >
        <p className="text-sm whitespace-pre-wrap">{message.text}</p>
      </div>
    </div>
  );
}
