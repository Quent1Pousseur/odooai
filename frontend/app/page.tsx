"use client";

import { useState, useRef, useEffect } from "react";
import { ChatMessage } from "@/components/chat-message";
import { ChatInput } from "@/components/chat-input";
import { OdooConnect } from "@/components/odoo-connect";
import { Sidebar } from "@/components/sidebar";

interface Message {
  role: "user" | "assistant";
  content: string;
  domain?: string;
  tokens?: number;
  sources?: string[];
}

interface ConversationItem {
  id: string;
  title: string;
  domain_id: string;
  updated_at: string;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [conversations, setConversations] = useState<ConversationItem[]>([]);
  const [currentConversationId, setCurrentConversationId] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [streamingText, setStreamingText] = useState("");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [odooCreds, setOdooCreds] = useState<{url: string; db: string; login: string; apiKey: string} | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    loadConversations();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, streamingText]);

  const loadConversations = async () => {
    try {
      const res = await fetch(`${API_URL}/api/conversations`);
      if (res.ok) setConversations(await res.json());
    } catch { /* API not available */ }
  };

  const loadMessages = async (conversationId: string) => {
    try {
      const res = await fetch(`${API_URL}/api/conversations/${conversationId}/messages`);
      if (res.ok) {
        const data = await res.json();
        setMessages(data.map((m: any) => ({ role: m.role, content: m.content, tokens: m.tokens })));
        setCurrentConversationId(conversationId);
      }
    } catch { /* API not available */ }
  };

  const handleNewConversation = () => {
    setMessages([]);
    setCurrentConversationId("");
    setStreamingText("");
  };

  const handleSend = async (question: string) => {
    setMessages((prev) => [...prev, { role: "user", content: question }]);
    setIsLoading(true);
    setStreamingText("");

    try {
      const response = await fetch(`${API_URL}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: question,
          conversation_id: currentConversationId,
          ...(odooCreds ? {
            odoo_url: odooCreds.url,
            odoo_db: odooCreds.db,
            odoo_login: odooCreds.login,
            odoo_api_key: odooCreds.apiKey,
          } : {}),
        }),
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);
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
        for (const line of chunk.split("\n")) {
          if (!line.startsWith("data: ")) continue;
          try {
            const data = JSON.parse(line.slice(6));
            if (data.type === "text") {
              fullText += data.content;
              setStreamingText(fullText);
            } else if (data.type === "domain") {
              domain = data.content;
            } else if (data.type === "conversation_id") {
              setCurrentConversationId(data.content);
            } else if (data.type === "tool_start") {
              fullText += `\n🔍 *Recherche (${data.tool})...*\n`;
              setStreamingText(fullText);
            } else if (data.type === "done") {
              tokens = data.tokens || 0;
              sources = data.sources || [];
            } else if (data.type === "error") {
              fullText = `Erreur: ${data.content}`;
              setStreamingText(fullText);
            }
          } catch { /* Skip malformed SSE */ }
        }
      }

      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: fullText, domain, tokens, sources },
      ]);
      setStreamingText("");
      loadConversations();
    } catch {
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
    <div className="flex h-screen">
      <Sidebar
        conversations={conversations}
        currentId={currentConversationId}
        onSelect={loadMessages}
        onNew={handleNewConversation}
        isOpen={sidebarOpen}
        onToggle={() => setSidebarOpen(!sidebarOpen)}
      />

      <div className="flex flex-col flex-1 min-w-0">
        <header className="bg-primary text-white p-4 flex items-center justify-between">
          <div>
            <h1 className="text-xl font-semibold">OdooAI</h1>
            <p className="text-sm text-accent">Votre Odoo peut faire plus.</p>
          </div>
          <OdooConnect
            isConnected={odooCreds !== null}
            onConnect={(creds) => setOdooCreds(creds)}
            onDisconnect={() => setOdooCreds(null)}
          />
        </header>

        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 && !isLoading && (
            <div className="text-center text-gray-400 mt-20">
              <p className="text-lg">Posez une question sur Odoo</p>
              <p className="text-sm mt-2">
                &quot;Comment automatiser mes relances ?&quot; · &quot;Quelles fonctionnalites je n&apos;utilise pas ?&quot;
              </p>
            </div>
          )}
          {messages.map((msg, i) => (
            <ChatMessage key={i} message={msg} />
          ))}
          {streamingText && (
            <ChatMessage message={{ role: "assistant", content: streamingText }} isStreaming />
          )}
          {isLoading && !streamingText && (
            <div className="text-gray-400 text-sm animate-pulse">Recherche en cours...</div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="text-xs text-gray-400 text-center px-4 py-1">
          OdooAI ne fournit pas de conseil juridique, fiscal ou comptable.
        </div>

        <ChatInput onSend={handleSend} isLoading={isLoading} />
      </div>
    </div>
  );
}
