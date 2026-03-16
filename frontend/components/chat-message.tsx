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
              }}
            >
              {message.content}
            </ReactMarkdown>
            {isStreaming && <span className="animate-pulse text-primary">|</span>}
          </div>
        )}

        {/* Metadata */}
        {!isUser && !isStreaming && message.tokens && (
          <div className="mt-3 text-xs text-gray-400 border-t border-gray-100 pt-2 flex items-center gap-2">
            <span>{message.tokens.toLocaleString()} tokens</span>
            {message.sources && message.sources.length > 0 && (
              <>
                <span className="text-gray-300">·</span>
                <span>{message.sources.join(", ")}</span>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
