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
        aria-label={isOpen ? "Fermer le menu" : "Ouvrir le menu"}
        className="md:hidden fixed top-3 left-3 z-50 bg-surface-sidebar text-white w-10 h-10 flex items-center justify-center rounded-xl shadow-lg hover:bg-surface-sidebar/90 transition-all"
      >
        {isOpen ? (
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M18 6L6 18M6 6l12 12" />
          </svg>
        ) : (
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M3 12h18M3 6h18M3 18h18" />
          </svg>
        )}
      </button>

      {/* Sidebar — dark theme */}
      <div
        className={`fixed md:static inset-y-0 left-0 z-40 w-72 bg-surface-sidebar
                     transform transition-transform duration-200
                     ${isOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"}`}
      >
        {/* Logo + New */}
        <div className="p-5">
          <div className="flex items-center gap-2.5 mb-5">
            <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-xs">AI</span>
            </div>
            <span className="text-white font-semibold text-sm tracking-tight">OdooAI</span>
          </div>
          <button
            onClick={onNew}
            className="w-full bg-white/10 hover:bg-white/15 text-white text-sm py-2.5 px-4 rounded-xl
                       transition-all flex items-center gap-2"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 5v14M5 12h14" />
            </svg>
            Nouvelle conversation
          </button>
        </div>

        {/* Conversation list */}
        <div className="px-3 overflow-y-auto h-[calc(100vh-140px)]">
          {conversations.length === 0 && (
            <p className="text-white/30 text-xs text-center mt-8">
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
              className={`w-full text-left px-3 py-2.5 rounded-xl mb-1 text-sm transition-all
                         ${currentId === conv.id
                           ? "bg-primary/30 text-white"
                           : "text-white/60 hover:bg-white/5 hover:text-white/80"}`}
            >
              <div className="truncate text-[13px]">
                {conv.title}
              </div>
              <div className="text-[11px] text-white/30 mt-0.5 flex items-center gap-1.5">
                {conv.domain_id && (
                  <span className="bg-white/10 px-1.5 py-0.5 rounded text-white/40">
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
          className="md:hidden fixed inset-0 bg-black/40 z-30 backdrop-blur-sm"
        />
      )}
    </>
  );
}
