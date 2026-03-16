"use client";

interface ConversationItem {
  id: string;
  title: string;
  domain_id: string;
  updated_at: string;
}

interface SidebarProps {
  conversations: ConversationItem[];
  currentId: string;
  onSelect: (id: string) => void;
  onNew: () => void;
  isOpen: boolean;
  onToggle: () => void;
}

export function Sidebar({
  conversations,
  currentId,
  onSelect,
  onNew,
  isOpen,
  onToggle,
}: SidebarProps) {
  return (
    <>
      {/* Mobile toggle */}
      <button
        onClick={onToggle}
        className="md:hidden fixed top-4 left-4 z-50 bg-primary text-white p-2 rounded-lg"
      >
        {isOpen ? "✕" : "☰"}
      </button>

      {/* Sidebar */}
      <div
        className={`fixed md:static inset-y-0 left-0 z-40 w-72 bg-white border-r border-gray-200
                     transform transition-transform duration-200
                     ${isOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"}`}
      >
        {/* Header */}
        <div className="p-4 border-b border-gray-200">
          <h2 className="text-sm font-semibold text-primary">OdooAI</h2>
          <button
            onClick={onNew}
            className="mt-2 w-full bg-primary text-white text-sm py-2 px-4 rounded-lg
                       hover:bg-primary/90 transition-colors"
          >
            + Nouvelle conversation
          </button>
        </div>

        {/* Conversation list */}
        <div className="overflow-y-auto h-[calc(100vh-120px)]">
          {conversations.length === 0 && (
            <p className="text-gray-400 text-sm text-center mt-8">
              Aucune conversation
            </p>
          )}
          {conversations.map((conv) => (
            <button
              key={conv.id}
              onClick={() => {
                onSelect(conv.id);
                onToggle();
              }}
              className={`w-full text-left px-4 py-3 border-b border-gray-100 text-sm
                         hover:bg-gray-50 transition-colors
                         ${currentId === conv.id ? "bg-accent/30 border-l-2 border-l-primary" : ""}`}
            >
              <div className="font-medium text-gray-800 truncate">
                {conv.title}
              </div>
              <div className="text-xs text-gray-400 mt-1">
                {conv.domain_id && (
                  <span className="bg-gray-100 px-1.5 py-0.5 rounded mr-1">
                    {conv.domain_id}
                  </span>
                )}
                {new Date(conv.updated_at).toLocaleDateString("fr-FR")}
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Overlay on mobile */}
      {isOpen && (
        <div
          onClick={onToggle}
          className="md:hidden fixed inset-0 bg-black/30 z-30"
        />
      )}
    </>
  );
}
