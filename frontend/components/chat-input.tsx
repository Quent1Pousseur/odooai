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
    <div className="bg-white border-t border-gray-100 px-4 py-3">
      <div className="flex gap-2 max-w-3xl mx-auto relative">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Demande-moi n'importe quoi sur ton Odoo..."
          disabled={isLoading}
          className="flex-1 bg-surface rounded-xl px-4 py-3 text-sm text-text
                     min-h-[48px] border border-gray-200
                     focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary/40
                     disabled:opacity-50
                     placeholder:text-text-muted
                     transition-all"
        />
        <button
          onClick={handleSubmit}
          disabled={isLoading || !input.trim()}
          className="bg-primary text-white px-4 py-3 rounded-xl
                     min-h-[48px] min-w-[48px]
                     hover:bg-primary-600 active:scale-[0.97]
                     disabled:opacity-30 disabled:cursor-not-allowed
                     transition-all flex items-center justify-center"
        >
          {isLoading ? (
            <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
          ) : (
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
              <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" />
            </svg>
          )}
        </button>
      </div>
    </div>
  );
}
