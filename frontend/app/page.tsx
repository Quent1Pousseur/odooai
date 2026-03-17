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

const QUICK_ACTIONS = [
  { emoji: "📊", text: "Mon CA du mois", question: "Quel est mon chiffre d'affaires ce mois-ci ?" },
  { emoji: "📦", text: "Stock critique", question: "Quels produits sont en rupture de stock ?" },
  { emoji: "💰", text: "Factures en retard", question: "Combien de factures sont impayees ?" },
  { emoji: "🚀", text: "Que puis-je ameliorer ?", question: "Qu'est-ce que je pourrais mieux faire avec Odoo ?" },
  { emoji: "📋", text: "Commandes du jour", question: "Mes commandes du jour ?" },
  { emoji: "⚡", text: "Challenge-moi", question: "Qu'est-ce que je fais a la main qu'Odoo pourrait automatiser ?" },
];

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
              const msg = data.message || "Recherche en cours";
              const model = data.model ? ` (${data.model})` : "";
              fullText += `\n> ${msg}${model}...\n\n`;
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
        {/* Header — clean, minimal */}
        <header className="bg-white border-b border-gray-100 px-6 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-[10px]">AI</span>
            </div>
            <div>
              <h1 className="text-sm font-semibold text-text">OdooAI</h1>
              <p className="text-[11px] text-text-muted">Ton buddy Odoo</p>
            </div>
          </div>
          <OdooConnect
            isConnected={odooCreds !== null}
            onConnect={(creds) => setOdooCreds(creds)}
            onDisconnect={() => setOdooCreds(null)}
          />
        </header>

        {/* Messages area */}
        <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4">
          <div className="max-w-3xl mx-auto space-y-4">
            {/* Empty state — buddy welcome */}
            {messages.length === 0 && !isLoading && (
              <div className="text-center mt-12 animate-fadeIn">
                <div className="w-16 h-16 bg-primary/10 rounded-2xl flex items-center justify-center mx-auto mb-5">
                  <span className="text-3xl">👋</span>
                </div>
                <h2 className="text-xl font-semibold text-text">
                  Salut ! Je suis ton buddy Odoo.
                </h2>
                <p className="text-sm text-text-light mt-2 max-w-lg mx-auto">
                  Je connais chaque fonctionnalite d&apos;Odoo. Demande-moi tes chiffres,
                  de la config, ou challenge-moi — je suis la pour t&apos;aider.
                </p>

                {/* Quick actions grid */}
                <div className="grid grid-cols-2 md:grid-cols-3 gap-2 mt-8 max-w-xl mx-auto">
                  {QUICK_ACTIONS.map((action) => (
                    <button
                      key={action.text}
                      onClick={() => handleSend(action.question)}
                      className="bg-white border border-gray-200 rounded-xl px-3 py-3
                                 text-left hover:border-primary/30 hover:shadow-soft
                                 transition-all group"
                    >
                      <span className="text-lg">{action.emoji}</span>
                      <p className="text-xs font-medium text-text mt-1 group-hover:text-primary transition-colors">
                        {action.text}
                      </p>
                    </button>
                  ))}
                </div>

                {/* Connection hint */}
                {!odooCreds && (
                  <p className="text-xs text-text-muted mt-6">
                    💡 Connecte ton Odoo pour des reponses personnalisees
                  </p>
                )}
              </div>
            )}

            {/* Messages */}
            {messages.map((msg, i) => (
              <ChatMessage key={i} message={msg} />
            ))}
            {streamingText && (
              <ChatMessage message={{ role: "assistant", content: streamingText }} isStreaming />
            )}
            {isLoading && !streamingText && (
              <div className="flex items-center gap-3 animate-fadeIn">
                <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center flex-shrink-0">
                  <span className="text-white font-bold text-[10px]">AI</span>
                </div>
                <div className="bg-white shadow-card rounded-2xl px-4 py-3 flex items-center gap-2">
                  <div className="w-4 h-4 border-2 border-primary/30 border-t-primary rounded-full animate-spin" />
                  <span className="text-sm text-text-light">Je regarde...</span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Disclaimer */}
        <div className="text-[11px] text-text-muted text-center px-4 py-1">
          OdooAI peut se tromper. Verifiez les informations importantes.
        </div>

        <ChatInput onSend={handleSend} isLoading={isLoading} />
      </div>
    </div>
  );
}
