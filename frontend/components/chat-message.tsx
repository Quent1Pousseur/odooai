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
        className={`max-w-[80%] rounded-lg px-4 py-3 ${
          isUser
            ? "bg-primary text-white"
            : "bg-white border border-gray-200 text-gray-800"
        }`}
      >
        {/* Domain badge */}
        {!isUser && message.domain && (
          <span className="inline-block text-xs bg-accent text-primary px-2 py-0.5 rounded mb-2">
            {message.domain}
          </span>
        )}

        {/* Content */}
        <div className="whitespace-pre-wrap text-sm leading-relaxed">
          {message.content}
          {isStreaming && <span className="animate-pulse">▊</span>}
        </div>

        {/* Metadata */}
        {!isUser && !isStreaming && message.tokens && (
          <div className="mt-2 text-xs text-gray-400 border-t border-gray-100 pt-1">
            {message.tokens} tokens
            {message.sources && message.sources.length > 0 && (
              <> · {message.sources.join(", ")}</>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
