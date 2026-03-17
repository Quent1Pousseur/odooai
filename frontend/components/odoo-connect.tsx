"use client";

import { useState, useEffect } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface OdooCredentials {
  url: string;
  db: string;
  login: string;
  apiKey: string;
}

interface SavedConnection {
  id: string;
  name: string;
  url: string;
  db_name: string;
  login: string;
  odoo_version: string;
  is_default: boolean;
  last_connected_at: string | null;
}

interface OdooConnectProps {
  onConnect: (creds: OdooCredentials) => void;
  onDisconnect: () => void;
  isConnected: boolean;
}

export function OdooConnect({ onConnect, onDisconnect, isConnected }: OdooConnectProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [tab, setTab] = useState<"saved" | "new">("saved");
  const [savedConnections, setSavedConnections] = useState<SavedConnection[]>([]);
  const [loading, setLoading] = useState(false);

  // New connection form
  const [name, setName] = useState("");
  const [url, setUrl] = useState("");
  const [db, setDb] = useState("");
  const [login, setLogin] = useState("");
  const [apiKey, setApiKey] = useState("");
  const [saveConnection, setSaveConnection] = useState(true);

  useEffect(() => {
    if (isOpen) loadConnections();
  }, [isOpen]);

  const loadConnections = async () => {
    try {
      const res = await fetch(`${API_URL}/api/connections`);
      if (res.ok) setSavedConnections(await res.json());
    } catch { /* API not available */ }
  };

  const handleConnectSaved = async (conn: SavedConnection) => {
    // For saved connections, we need the API key from the backend
    // The chat endpoint will use the connection ID to decrypt
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/api/connections/${conn.id}/test`, { method: "POST" });
      const data = await res.json();
      if (data.status === "ok") {
        // Store connection info — the chat will use connection_id
        onConnect({ url: conn.url, db: conn.db_name, login: conn.login, apiKey: `connection:${conn.id}` });
        setIsOpen(false);
      } else {
        alert(`Connexion echouee : ${data.error}`);
      }
    } catch {
      alert("Impossible de tester la connexion");
    } finally {
      setLoading(false);
    }
  };

  const handleConnectNew = async () => {
    if (!url || !db || !login || !apiKey) return;
    setLoading(true);

    if (saveConnection && name) {
      try {
        await fetch(`${API_URL}/api/connections`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ name, url, db_name: db, login, api_key: apiKey }),
        });
      } catch { /* Save failed, still connect */ }
    }

    onConnect({ url, db, login, apiKey });
    setIsOpen(false);
    setLoading(false);
  };

  const handleDelete = async (id: string) => {
    try {
      await fetch(`${API_URL}/api/connections/${id}`, { method: "DELETE" });
      setSavedConnections((prev) => prev.filter((c) => c.id !== id));
    } catch { /* ignore */ }
  };

  if (isConnected) {
    return (
      <div className="flex items-center gap-2">
        <div className="flex items-center gap-1.5 bg-green-50 px-2.5 py-1 rounded-lg">
          <div className="w-2 h-2 bg-success rounded-full" />
          <span className="text-xs text-success font-medium">Connecte</span>
        </div>
        <button onClick={onDisconnect} className="text-xs text-text-muted hover:text-text transition-colors">
          Deconnecter
        </button>
      </div>
    );
  }

  return (
    <>
      <button
        onClick={() => setIsOpen(true)}
        className="text-xs bg-primary/10 text-primary font-medium px-3 py-1.5 rounded-lg hover:bg-primary/20 transition-all"
      >
        Connecter Odoo
      </button>

      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm">
          <div className="bg-white rounded-2xl shadow-lg w-full max-w-md mx-4 animate-fadeIn overflow-hidden">
            {/* Header */}
            <div className="flex items-center gap-3 p-5 pb-0">
              <div className="w-10 h-10 bg-primary/10 rounded-xl flex items-center justify-center">
                <svg className="w-5 h-5 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                  <path d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101" />
                  <path d="M10.172 13.828a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.102 1.101" />
                </svg>
              </div>
              <div>
                <h3 className="text-base font-semibold text-text">Connecter Odoo</h3>
                <p className="text-xs text-text-muted">Choisis une connexion ou ajoute-en une</p>
              </div>
            </div>

            {/* Tabs */}
            <div className="flex gap-1 px-5 mt-4">
              <button
                onClick={() => setTab("saved")}
                className={`flex-1 text-xs font-medium py-2 rounded-lg transition-all ${
                  tab === "saved" ? "bg-primary text-white" : "bg-surface text-text-muted hover:text-text"
                }`}
              >
                Connexions ({savedConnections.length})
              </button>
              <button
                onClick={() => setTab("new")}
                className={`flex-1 text-xs font-medium py-2 rounded-lg transition-all ${
                  tab === "new" ? "bg-primary text-white" : "bg-surface text-text-muted hover:text-text"
                }`}
              >
                + Nouvelle
              </button>
            </div>

            <div className="p-5">
              {/* Saved connections tab */}
              {tab === "saved" && (
                <div className="space-y-2">
                  {savedConnections.length === 0 && (
                    <div className="text-center py-6">
                      <p className="text-sm text-text-muted">Aucune connexion sauvegardee</p>
                      <button
                        onClick={() => setTab("new")}
                        className="text-xs text-primary font-medium mt-2 hover:underline"
                      >
                        Ajouter une connexion
                      </button>
                    </div>
                  )}
                  {savedConnections.map((conn) => (
                    <div
                      key={conn.id}
                      className="flex items-center gap-3 p-3 rounded-xl border border-gray-200 hover:border-primary/30 transition-all group"
                    >
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-text truncate">{conn.name}</p>
                        <p className="text-[11px] text-text-muted truncate">{conn.url} · {conn.db_name}</p>
                      </div>
                      <button
                        onClick={() => handleDelete(conn.id)}
                        className="text-text-muted hover:text-danger p-1 opacity-0 group-hover:opacity-100 transition-all"
                        title="Supprimer"
                      >
                        <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                          <path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                      <button
                        onClick={() => handleConnectSaved(conn)}
                        disabled={loading}
                        className="bg-primary text-white text-xs font-medium px-3 py-1.5 rounded-lg hover:bg-primary-600 disabled:opacity-40 transition-all"
                      >
                        {loading ? "..." : "Connecter"}
                      </button>
                    </div>
                  ))}
                </div>
              )}

              {/* New connection tab */}
              {tab === "new" && (
                <div className="space-y-3">
                  <div>
                    <label className="block text-xs font-medium text-text-light mb-1">Nom de la connexion</label>
                    <input
                      type="text"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      placeholder="Mon Odoo Production"
                      className="w-full bg-surface border border-gray-200 rounded-xl px-3 py-2.5 text-sm text-text focus:ring-2 focus:ring-primary/20 focus:border-primary/40 focus:outline-none transition-all"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-text-light mb-1">URL</label>
                    <input
                      type="url"
                      value={url}
                      onChange={(e) => setUrl(e.target.value)}
                      placeholder="https://mon-odoo.com"
                      className="w-full bg-surface border border-gray-200 rounded-xl px-3 py-2.5 text-sm text-text focus:ring-2 focus:ring-primary/20 focus:border-primary/40 focus:outline-none transition-all"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-text-light mb-1">Base de donnees</label>
                    <input
                      type="text"
                      value={db}
                      onChange={(e) => setDb(e.target.value)}
                      placeholder="ma-base"
                      className="w-full bg-surface border border-gray-200 rounded-xl px-3 py-2.5 text-sm text-text focus:ring-2 focus:ring-primary/20 focus:border-primary/40 focus:outline-none transition-all"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-text-light mb-1">Login</label>
                    <input
                      type="email"
                      value={login}
                      onChange={(e) => setLogin(e.target.value)}
                      placeholder="admin@monentreprise.com"
                      className="w-full bg-surface border border-gray-200 rounded-xl px-3 py-2.5 text-sm text-text focus:ring-2 focus:ring-primary/20 focus:border-primary/40 focus:outline-none transition-all"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-text-light mb-1">Cle API</label>
                    <input
                      type="password"
                      value={apiKey}
                      onChange={(e) => setApiKey(e.target.value)}
                      placeholder="Cle API Odoo"
                      className="w-full bg-surface border border-gray-200 rounded-xl px-3 py-2.5 text-sm text-text focus:ring-2 focus:ring-primary/20 focus:border-primary/40 focus:outline-none transition-all"
                    />
                    <p className="text-[11px] text-text-muted mt-1">
                      Odoo &gt; Parametres &gt; Utilisateurs &gt; Cles API
                    </p>
                  </div>
                  <label className="flex items-center gap-2 mt-1">
                    <input
                      type="checkbox"
                      checked={saveConnection}
                      onChange={(e) => setSaveConnection(e.target.checked)}
                      className="rounded border-gray-300 text-primary focus:ring-primary/20"
                    />
                    <span className="text-xs text-text-light">Sauvegarder cette connexion (chiffree)</span>
                  </label>
                </div>
              )}
            </div>

            {/* Footer */}
            <div className="flex gap-2 px-5 pb-5">
              <button
                onClick={() => setIsOpen(false)}
                className="flex-1 bg-surface text-text py-2.5 rounded-xl text-sm font-medium hover:bg-surface-hover transition-all"
              >
                Annuler
              </button>
              {tab === "new" && (
                <button
                  onClick={handleConnectNew}
                  disabled={!url || !db || !login || !apiKey || loading}
                  className="flex-1 bg-primary text-white py-2.5 rounded-xl text-sm font-medium hover:bg-primary-600 disabled:opacity-40 transition-all"
                >
                  {loading ? "Connexion..." : "Connecter"}
                </button>
              )}
            </div>
          </div>
        </div>
      )}
    </>
  );
}
