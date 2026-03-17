"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";

interface Message {
  role: "user" | "assistant";
  content: string;
  domain?: string;
  tokens?: number;
  sources?: string[];
}

interface ChatMessageProps {
  message: Message;
  isStreaming?: boolean;
}

export function ChatMessage({ message, isStreaming }: ChatMessageProps) {
  const isUser = message.role === "user";
  const [copied, setCopied] = useState(false);
  const [feedback, setFeedback] = useState<"up" | "down" | null>(null);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} animate-fadeIn`}>
      <div className={`max-w-[85%] ${isUser ? "" : "flex gap-3"}`}>
        {/* Avatar for AI */}
        {!isUser && (
          <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center flex-shrink-0 mt-1">
            <span className="text-white font-bold text-[10px]">AI</span>
          </div>
        )}

        <div
          className={`rounded-2xl px-4 py-3 ${
            isUser
              ? "bg-primary text-white shadow-soft"
              : "bg-white shadow-card text-text"
          }`}
        >
          {/* Domain badge */}
          {!isUser && message.domain && (
            <span className="inline-block text-[11px] font-medium bg-primary-50 text-primary px-2 py-0.5 rounded-full mb-2">
              {message.domain}
            </span>
          )}

          {/* Content */}
          {isUser ? (
            <div className="text-sm leading-relaxed">{message.content}</div>
          ) : (
            <div className="text-sm leading-relaxed">
              <ReactMarkdown
                components={{
                  h1: ({ children }) => (
                    <h3 className="text-[15px] font-semibold text-text mt-3 mb-1.5 first:mt-0">{children}</h3>
                  ),
                  h2: ({ children }) => (
                    <h3 className="text-[15px] font-semibold text-text mt-3 mb-1.5 first:mt-0">{children}</h3>
                  ),
                  h3: ({ children }) => (
                    <h4 className="text-sm font-semibold text-text mt-2 mb-1">{children}</h4>
                  ),
                  p: ({ children }) => (
                    <p className="text-sm leading-relaxed text-text mb-2 last:mb-0">{children}</p>
                  ),
                  ul: ({ children }) => (
                    <ul className="text-sm space-y-0.5 ml-4 mb-2 list-disc text-text">{children}</ul>
                  ),
                  ol: ({ children }) => (
                    <ol className="text-sm space-y-0.5 ml-4 mb-2 list-decimal text-text">{children}</ol>
                  ),
                  li: ({ children }) => (
                    <li className="leading-relaxed">{children}</li>
                  ),
                  strong: ({ children }) => (
                    <strong className="font-semibold text-gray-900">{children}</strong>
                  ),
                  em: ({ children }) => (
                    <em className="text-text-muted not-italic text-xs">{children}</em>
                  ),
                  hr: () => <hr className="my-3 border-gray-100" />,
                  code: ({ children }) => (
                    <code className="text-xs bg-primary-50 text-primary-700 px-1.5 py-0.5 rounded font-mono">{children}</code>
                  ),
                  blockquote: ({ children }) => (
                    <div className="flex items-center gap-2 bg-accent-50 border-l-2 border-accent px-3 py-2 rounded-r-lg mb-2">
                      <div className="w-3.5 h-3.5 border-2 border-accent rounded-full border-t-transparent animate-spin flex-shrink-0" />
                      <span className="text-xs text-accent-600 font-medium">{children}</span>
                    </div>
                  ),
                  table: ({ children }) => (
                    <div className="overflow-x-auto my-2">
                      <table className="text-xs w-full border-collapse">{children}</table>
                    </div>
                  ),
                  thead: ({ children }) => (
                    <thead className="bg-surface">{children}</thead>
                  ),
                  th: ({ children }) => (
                    <th className="text-left px-2.5 py-1.5 font-semibold text-text-light border-b border-gray-100">{children}</th>
                  ),
                  td: ({ children }) => (
                    <td className="px-2.5 py-1.5 border-b border-gray-50">{children}</td>
                  ),
                }}
              >
                {message.content}
              </ReactMarkdown>
              {isStreaming && <span className="animate-pulse text-primary ml-0.5">|</span>}
            </div>
          )}

          {/* Actions */}
          {!isUser && !isStreaming && message.content && (
            <div className="mt-2 flex items-center gap-0.5 pt-2 border-t border-gray-50">
              <button
                onClick={handleCopy}
                className="text-text-muted hover:text-text p-1.5 rounded-lg hover:bg-surface transition-all"
                title="Copier"
              >
                {copied ? (
                  <svg className="w-3.5 h-3.5 text-success" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                  </svg>
                ) : (
                  <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                    <rect x="9" y="9" width="13" height="13" rx="2" />
                    <path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1" />
                  </svg>
                )}
              </button>
              <button
                onClick={() => setFeedback(feedback === "up" ? null : "up")}
                className={`p-1.5 rounded-lg transition-all ${
                  feedback === "up" ? "text-success bg-green-50" : "text-text-muted hover:text-text hover:bg-surface"
                }`}
              >
                <svg className="w-3.5 h-3.5" fill={feedback === "up" ? "currentColor" : "none"} viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                  <path d="M14 9V5a3 3 0 00-3-3l-4 9v11h11.28a2 2 0 002-1.7l1.38-9a2 2 0 00-2-2.3H14z" />
                </svg>
              </button>
              <button
                onClick={() => setFeedback(feedback === "down" ? null : "down")}
                className={`p-1.5 rounded-lg transition-all ${
                  feedback === "down" ? "text-danger bg-red-50" : "text-text-muted hover:text-text hover:bg-surface"
                }`}
              >
                <svg className="w-3.5 h-3.5" fill={feedback === "down" ? "currentColor" : "none"} viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                  <path d="M10 15v3.586a1 1 0 01-.293.707l-2 2A1 1 0 016 20.586V15H3a2 2 0 01-2-2.3l1.38-9A2 2 0 014.28 2H14v11z" />
                </svg>
              </button>
              {message.tokens && (
                <span className="ml-auto text-[11px] text-text-muted">
                  {message.tokens.toLocaleString()} tokens
                </span>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
