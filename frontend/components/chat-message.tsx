"use client";

import { useState, useCallback } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import { DashboardArtifact, tryParseDashboard } from "./dashboard-artifact";

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

function hasMarkdownTable(content: string): boolean {
  const lines = content.split("\n");
  let pipeLines = 0;
  for (const line of lines) {
    if (line.includes("|") && line.trim().startsWith("|")) {
      pipeLines++;
      if (pipeLines >= 2) return true;
    }
  }
  return false;
}

function markdownTableToCsv(content: string): string {
  const lines = content.split("\n");
  const tableLines = lines.filter(
    (line) => line.includes("|") && line.trim().startsWith("|")
  );
  const csvRows: string[] = [];
  for (const line of tableLines) {
    const cells = line
      .split("|")
      .slice(1, -1)
      .map((cell) => cell.trim());
    // Skip separator lines (e.g. |---|---|)
    if (cells.every((c) => /^[-:]+$/.test(c))) continue;
    // Escape cells that contain commas or quotes
    const escaped = cells.map((c) => {
      if (c.includes(",") || c.includes('"') || c.includes("\n")) {
        return `"${c.replace(/"/g, '""')}"`;
      }
      return c;
    });
    csvRows.push(escaped.join(","));
  }
  return csvRows.join("\n");
}

function CodeBlockCopyButton({ code }: { code: string }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <button
      onClick={handleCopy}
      className="absolute top-2 right-2 text-gray-400 hover:text-gray-200 bg-gray-800 hover:bg-gray-700 p-1.5 rounded-md transition-all text-[11px] font-mono"
      title="Copy code"
    >
      {copied ? (
        <svg className="w-3.5 h-3.5 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5">
          <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
        </svg>
      ) : (
        <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
          <rect x="9" y="9" width="13" height="13" rx="2" />
          <path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1" />
        </svg>
      )}
    </button>
  );
}

export function ChatMessage({ message, isStreaming }: ChatMessageProps) {
  const isUser = message.role === "user";
  const [copied, setCopied] = useState(false);
  const [feedback, setFeedback] = useState<"up" | "down" | null>(null);

  // Detect dashboard artifacts
  const parsed = !isUser ? tryParseDashboard(message.content) : null;
  const hasDashboard = parsed?.dashboard != null;
  const markdownContent = hasDashboard
    ? (parsed!.before + "\n" + parsed!.after).trim()
    : message.content;

  const handleCopy = async () => {
    await navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleExportCsv = useCallback(() => {
    const csvContent = markdownTableToCsv(message.content);
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "odooai-export.csv";
    a.click();
    URL.revokeObjectURL(url);
  }, [message.content]);

  const showExportCsv = !isUser && hasMarkdownTable(message.content);

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
              {hasDashboard && parsed?.dashboard && (
                <DashboardArtifact data={parsed.dashboard} />
              )}
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={{
                  h1: ({ children }) => (
                    <h1 className="text-base font-bold text-text mt-4 mb-2 first:mt-0">{children}</h1>
                  ),
                  h2: ({ children }) => (
                    <h2 className="text-[15px] font-bold text-text mt-4 mb-2 first:mt-0">{children}</h2>
                  ),
                  h3: ({ children }) => (
                    <h3 className="text-sm font-semibold text-text mt-3 mb-1.5 first:mt-0">{children}</h3>
                  ),
                  p: ({ children }) => (
                    <p className="text-sm leading-relaxed text-text mb-3 last:mb-0">{children}</p>
                  ),
                  ul: ({ children }) => (
                    <ul className="text-sm space-y-1.5 ml-5 mb-3 list-disc list-outside text-text">{children}</ul>
                  ),
                  ol: ({ children }) => (
                    <ol className="text-sm space-y-1.5 ml-5 mb-3 list-decimal list-outside text-text">{children}</ol>
                  ),
                  li: ({ children }) => (
                    <li className="leading-relaxed pl-0.5">{children}</li>
                  ),
                  strong: ({ children }) => (
                    <strong className="font-semibold text-gray-900">{children}</strong>
                  ),
                  em: ({ children }) => (
                    <em className="italic text-text-light">{children}</em>
                  ),
                  hr: () => <hr className="my-4 border-t border-gray-200" />,
                  code: ({ className, children, ...props }) => {
                    const match = /language-(\w+)/.exec(className || "");
                    const codeString = String(children).replace(/\n$/, "");

                    if (match) {
                      return (
                        <SyntaxHighlighter
                          style={oneDark}
                          language={match[1]}
                          PreTag="div"
                          customStyle={{
                            margin: 0,
                            padding: "1rem",
                            fontSize: "0.75rem",
                            lineHeight: "1.625",
                            background: "transparent",
                          }}
                        >
                          {codeString}
                        </SyntaxHighlighter>
                      );
                    }

                    return (
                      <code
                        className="text-xs bg-gray-100 text-primary-700 px-1.5 py-0.5 rounded font-mono border border-gray-200"
                        {...props}
                      >
                        {children}
                      </code>
                    );
                  },
                  pre: ({ children }) => {
                    // Extract code string for copy button
                    let codeString = "";
                    if (
                      children &&
                      typeof children === "object" &&
                      "props" in (children as React.ReactElement)
                    ) {
                      const childProps = (children as React.ReactElement).props;
                      codeString = String(childProps.children || "").replace(/\n$/, "");
                    }

                    return (
                      <div className="my-3 overflow-hidden rounded-lg bg-gray-900 relative group">
                        <CodeBlockCopyButton code={codeString} />
                        <div className="overflow-x-auto">
                          <pre className="text-xs leading-relaxed text-gray-100 font-mono">
                            {children}
                          </pre>
                        </div>
                      </div>
                    );
                  },
                  blockquote: ({ children }) => (
                    <div className="border-l-4 border-primary/30 pl-3 py-1 my-2 bg-primary-50/50 rounded-r">
                      <div className="text-sm text-text-light">{children}</div>
                    </div>
                  ),
                  table: ({ children }) => (
                    <div className="overflow-x-auto my-3 rounded-lg border border-gray-200">
                      <table className="w-full text-xs border-collapse">{children}</table>
                    </div>
                  ),
                  thead: ({ children }) => (
                    <thead className="bg-gray-50 border-b border-gray-200">{children}</thead>
                  ),
                  tbody: ({ children }) => (
                    <tbody className="divide-y divide-gray-100">{children}</tbody>
                  ),
                  tr: ({ children }) => (
                    <tr className="hover:bg-gray-50/50 transition-colors">{children}</tr>
                  ),
                  th: ({ children }) => (
                    <th className="text-left px-3 py-2 font-semibold text-text text-xs whitespace-nowrap">{children}</th>
                  ),
                  td: ({ children }) => (
                    <td className="px-3 py-2 text-text">{children}</td>
                  ),
                  a: ({ href, children }) => (
                    <a href={href} className="text-primary font-medium underline hover:text-primary-700 transition-colors" target="_blank" rel="noopener noreferrer">{children}</a>
                  ),
                }}
              >
                {markdownContent}
              </ReactMarkdown>
              {isStreaming && <span className="animate-pulse text-primary ml-0.5">|</span>}
            </div>
          )}

          {/* Actions */}
          {!isUser && !isStreaming && message.content && (
            <div className="mt-2 flex items-center gap-0.5 pt-2 border-t border-gray-50">
              <button onClick={handleCopy} className="text-text-muted hover:text-text p-1.5 rounded-lg hover:bg-surface transition-all" title="Copier">
                {copied ? (
                  <svg className="w-3.5 h-3.5 text-success" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5"><path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" /></svg>
                ) : (
                  <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2"><rect x="9" y="9" width="13" height="13" rx="2" /><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1" /></svg>
                )}
              </button>
              <button onClick={() => setFeedback(feedback === "up" ? null : "up")} className={`p-1.5 rounded-lg transition-all ${feedback === "up" ? "text-success bg-green-50" : "text-text-muted hover:text-text hover:bg-surface"}`}>
                <svg className="w-3.5 h-3.5" fill={feedback === "up" ? "currentColor" : "none"} viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2"><path d="M14 9V5a3 3 0 00-3-3l-4 9v11h11.28a2 2 0 002-1.7l1.38-9a2 2 0 00-2-2.3H14z" /></svg>
              </button>
              <button onClick={() => setFeedback(feedback === "down" ? null : "down")} className={`p-1.5 rounded-lg transition-all ${feedback === "down" ? "text-danger bg-red-50" : "text-text-muted hover:text-text hover:bg-surface"}`}>
                <svg className="w-3.5 h-3.5" fill={feedback === "down" ? "currentColor" : "none"} viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2"><path d="M10 15v3.586a1 1 0 01-.293.707l-2 2A1 1 0 016 20.586V15H3a2 2 0 01-2-2.3l1.38-9A2 2 0 014.28 2H14v11z" /></svg>
              </button>
              {showExportCsv && (
                <button
                  onClick={handleExportCsv}
                  className="text-text-muted hover:text-text p-1.5 rounded-lg hover:bg-surface transition-all flex items-center gap-1"
                  title="Export CSV"
                >
                  <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <span className="text-[11px]">Export</span>
                </button>
              )}
              {message.tokens && (
                <span className="ml-auto text-[11px] text-text-muted">{message.tokens.toLocaleString()} tokens</span>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
