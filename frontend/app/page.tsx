"use client";

import { useState, useRef, useEffect } from "react";
import { ChatMessage } from "@/components/chat-message";
import { ChatInput } from "@/components/chat-input";

interface Message {
  role: "user" | "assistant";
  content: string;
  domain?: string;
  tokens?: number;
  sources?: string[];
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [streamingText, setStreamingText] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, streamingText]);

  const handleSend = async (question: string) => {
    // Add user message
    setMessages((prev) => [...prev, { role: "user", content: question }]);
    setIsLoading(true);
    setStreamingText("");

    try {
      const response = await fetch(`${API_URL}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: question }),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const reader = response.body?.getReader();
      if (!reader) throw new Error("No reader");

      const decoder = new TextDecoder();
      let fullText = "";
      let domain = "";
      let tokens = 0;
      let sources: string[] = [];

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split("\n");

        for (const line of lines) {
          if (!line.startsWith("data: ")) continue;
          try {
            const data = JSON.parse(line.slice(6));
            if (data.type === "text") {
              fullText += data.content;
              setStreamingText(fullText);
            } else if (data.type === "domain") {
              domain = data.content;
            } else if (data.type === "tool_start") {
              fullText += `\n🔍 *Recherche dans Odoo (${data.tool})...*\n`;
              setStreamingText(fullText);
            } else if (data.type === "tool_end") {
              // Tool finished, LLM will continue
            } else if (data.type === "status") {
              fullText += `\n_${data.content}_\n`;
              setStreamingText(fullText);
            } else if (data.type === "done") {
              tokens = data.tokens || 0;
              sources = data.sources || [];
            } else if (data.type === "error") {
              fullText = `Erreur: ${data.content}`;
              setStreamingText(fullText);
            }
          } catch {
            // Skip malformed SSE lines
          }
        }
      }

      // Add assistant message
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: fullText, domain, tokens, sources },
      ]);
      setStreamingText("");
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Erreur de connexion au serveur." },
      ]);
    } finally {
      setIsLoading(false);
      setStreamingText("");
    }
  };

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto">
      {/* Header */}
      <header className="bg-primary text-white p-4 text-center">
        <h1 className="text-xl font-semibold">OdooAI</h1>
        <p className="text-sm text-accent">Votre Odoo peut faire plus.</p>
      </header>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && !isLoading && (
          <div className="text-center text-gray-400 mt-20">
            <p className="text-lg">Posez une question sur Odoo</p>
            <p className="text-sm mt-2">
              Exemples : &quot;Comment automatiser mes relances ?&quot;,
              &quot;Quelles fonctionnalites de stock je n&apos;utilise pas ?&quot;
            </p>
          </div>
        )}

        {messages.map((msg, i) => (
          <ChatMessage key={i} message={msg} />
        ))}

        {streamingText && (
          <ChatMessage
            message={{ role: "assistant", content: streamingText }}
            isStreaming
          />
        )}

        {isLoading && !streamingText && (
          <div className="text-gray-400 text-sm animate-pulse">
            Recherche en cours...
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Disclaimer */}
      <div className="text-xs text-gray-400 text-center px-4 py-1">
        OdooAI ne fournit pas de conseil juridique, fiscal ou comptable.
      </div>

      {/* Input */}
      <ChatInput onSend={handleSend} isLoading={isLoading} />
    </div>
  );
}
