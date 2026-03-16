"use client";

import { useState, KeyboardEvent } from "react";

interface ChatInputProps {
  onSend: (message: string) => void;
  isLoading: boolean;
}

export function ChatInput({ onSend, isLoading }: ChatInputProps) {
  const [input, setInput] = useState("");

  const handleSubmit = () => {
    const trimmed = input.trim();
    if (!trimmed || isLoading) return;
    onSend(trimmed);
    setInput("");
  };

  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="bg-white px-6 py-4">
      <div className="flex gap-3 max-w-4xl mx-auto">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Posez votre question sur Odoo..."
          disabled={isLoading}
          className="flex-1 border border-gray-200 rounded-xl px-4 py-3 text-sm text-gray-900
                     min-h-[48px]
                     focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary
                     disabled:bg-gray-50 disabled:text-gray-400
                     placeholder:text-gray-400
                     transition-all"
        />
        <button
          onClick={handleSubmit}
          disabled={isLoading || !input.trim()}
          className="bg-primary text-white px-5 py-3 rounded-xl text-sm font-medium
                     min-h-[48px] min-w-[100px]
                     hover:bg-primary/90 active:scale-[0.98]
                     disabled:opacity-40 disabled:cursor-not-allowed
                     transition-all"
        >
          {isLoading ? (
            <span className="flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 bg-white/60 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
              <span className="w-1.5 h-1.5 bg-white/60 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
              <span className="w-1.5 h-1.5 bg-white/60 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
            </span>
          ) : "Envoyer"}
        </button>
      </div>
    </div>
  );
}
