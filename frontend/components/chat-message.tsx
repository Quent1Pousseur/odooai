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
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[80%] rounded-2xl px-5 py-4 shadow-sm ${
          isUser
            ? "bg-primary text-white"
            : "bg-white border border-gray-100 text-gray-800"
        }`}
      >
        {/* Domain badge */}
        {!isUser && message.domain && (
          <span className="inline-block text-xs font-medium bg-accent/20 text-primary px-2.5 py-1 rounded-full mb-3">
            {message.domain}
          </span>
        )}

        {/* Content */}
        {isUser ? (
          <div className="text-sm leading-relaxed">{message.content}</div>
        ) : (
          <div className="prose prose-sm prose-gray max-w-none">
            <ReactMarkdown
              components={{
                h1: ({ children }) => (
                  <h3 className="text-base font-semibold text-primary mt-4 mb-2 first:mt-0">{children}</h3>
                ),
                h2: ({ children }) => (
                  <h3 className="text-base font-semibold text-primary mt-4 mb-2 first:mt-0">{children}</h3>
                ),
                h3: ({ children }) => (
                  <h4 className="text-sm font-semibold text-gray-800 mt-3 mb-1">{children}</h4>
                ),
                p: ({ children }) => (
                  <p className="text-sm leading-relaxed text-gray-700 mb-2">{children}</p>
                ),
                ul: ({ children }) => (
                  <ul className="text-sm space-y-1 ml-4 mb-3 list-disc text-gray-700">{children}</ul>
                ),
                ol: ({ children }) => (
                  <ol className="text-sm space-y-1 ml-4 mb-3 list-decimal text-gray-700">{children}</ol>
                ),
                li: ({ children }) => (
                  <li className="leading-relaxed">{children}</li>
                ),
                strong: ({ children }) => (
                  <strong className="font-semibold text-gray-900">{children}</strong>
                ),
                em: ({ children }) => (
                  <em className="text-gray-500 not-italic text-xs">{children}</em>
                ),
                hr: () => <hr className="my-3 border-gray-200" />,
                code: ({ children }) => (
                  <code className="text-xs bg-gray-100 text-primary px-1.5 py-0.5 rounded font-mono">{children}</code>
                ),
                blockquote: ({ children }) => (
                  <div className="flex items-center gap-2 bg-blue-50 border-l-3 border-primary px-3 py-2 rounded-r-lg mb-2">
                    <svg className="w-4 h-4 text-primary animate-spin flex-shrink-0" viewBox="0 0 24 24" fill="none">
                      <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" opacity="0.3" />
                      <path d="M12 2a10 10 0 019.95 9" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                    </svg>
                    <span className="text-xs text-primary font-medium">{children}</span>
                  </div>
                ),
              }}
            >
              {message.content}
            </ReactMarkdown>
            {isStreaming && <span className="animate-pulse text-primary">|</span>}
          </div>
        )}

        {/* Actions — Copy + Feedback */}
        {!isUser && !isStreaming && message.content && (
          <div className="mt-3 flex items-center gap-1 border-t border-gray-100 pt-2">
            {/* Copy button */}
            <button
              onClick={handleCopy}
              className="text-gray-400 hover:text-gray-600 p-1.5 rounded-lg hover:bg-gray-50 transition-all"
              title="Copier la reponse"
            >
              {copied ? (
                <svg className="w-4 h-4 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                </svg>
              ) : (
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                  <rect x="9" y="9" width="13" height="13" rx="2" ry="2" />
                  <path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1" />
                </svg>
              )}
            </button>

            {/* Feedback thumbs */}
            <button
              onClick={() => setFeedback(feedback === "up" ? null : "up")}
              className={`p-1.5 rounded-lg transition-all ${
                feedback === "up"
                  ? "text-green-500 bg-green-50"
                  : "text-gray-400 hover:text-gray-600 hover:bg-gray-50"
              }`}
              title="Reponse utile"
            >
              <svg className="w-4 h-4" fill={feedback === "up" ? "currentColor" : "none"} viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                <path strokeLinecap="round" strokeLinejoin="round" d="M14 9V5a3 3 0 00-3-3l-4 9v11h11.28a2 2 0 002-1.7l1.38-9a2 2 0 00-2-2.3H14z" />
              </svg>
            </button>
            <button
              onClick={() => setFeedback(feedback === "down" ? null : "down")}
              className={`p-1.5 rounded-lg transition-all ${
                feedback === "down"
                  ? "text-red-500 bg-red-50"
                  : "text-gray-400 hover:text-gray-600 hover:bg-gray-50"
              }`}
              title="Reponse pas utile"
            >
              <svg className="w-4 h-4" fill={feedback === "down" ? "currentColor" : "none"} viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                <path strokeLinecap="round" strokeLinejoin="round" d="M10 15v3.586a1 1 0 01-.293.707l-2 2A1 1 0 016 20.586V15H3a2 2 0 01-2-2.3l1.38-9A2 2 0 014.28 2H14v11z" />
              </svg>
            </button>

            {/* Metadata */}
            <div className="ml-auto text-xs text-gray-400 flex items-center gap-2">
              {message.tokens && <span>{message.tokens.toLocaleString()} tokens</span>}
              {message.sources && message.sources.length > 0 && (
                <>
                  <span className="text-gray-300">·</span>
                  <span>{message.sources.join(", ")}</span>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
