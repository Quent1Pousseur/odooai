"use client";

import { useState } from "react";

interface OdooCredentials {
  url: string;
  db: string;
  login: string;
  apiKey: string;
}

interface OdooConnectProps {
  onConnect: (creds: OdooCredentials) => void;
  onDisconnect: () => void;
  isConnected: boolean;
}

export function OdooConnect({ onConnect, onDisconnect, isConnected }: OdooConnectProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [url, setUrl] = useState("");
  const [db, setDb] = useState("");
  const [login, setLogin] = useState("");
  const [apiKey, setApiKey] = useState("");

  const handleSubmit = () => {
    if (!url || !db || !login || !apiKey) return;
    onConnect({ url, db, login, apiKey });
    setIsOpen(false);
  };

  if (isConnected) {
    return (
      <div className="flex items-center gap-2">
        <div className="flex items-center gap-1.5 bg-green-50 px-2.5 py-1 rounded-lg">
          <div className="w-2 h-2 bg-success rounded-full" />
          <span className="text-xs text-success font-medium">Connecte</span>
        </div>
        <button
          onClick={onDisconnect}
          className="text-xs text-text-muted hover:text-text transition-colors"
        >
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
          <div className="bg-white rounded-2xl shadow-lg p-6 w-full max-w-md mx-4 animate-fadeIn">
            <div className="flex items-center gap-3 mb-5">
              <div className="w-10 h-10 bg-primary/10 rounded-xl flex items-center justify-center">
                <svg className="w-5 h-5 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                  <path d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101" />
                  <path d="M10.172 13.828a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.102 1.101" />
                </svg>
              </div>
              <div>
                <h3 className="text-base font-semibold text-text">Connecter ton Odoo</h3>
                <p className="text-xs text-text-muted">Tes donnees ne sont pas stockees</p>
              </div>
            </div>

            <div className="space-y-3">
              <div>
                <label className="block text-xs font-medium text-text-light mb-1">URL</label>
                <input
                  type="url"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  placeholder="https://mon-odoo.com"
                  className="w-full bg-surface border border-gray-200 rounded-xl px-3 py-2.5 text-sm text-text
                             focus:ring-2 focus:ring-primary/20 focus:border-primary/40 focus:outline-none transition-all"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-text-light mb-1">Base de donnees</label>
                <input
                  type="text"
                  value={db}
                  onChange={(e) => setDb(e.target.value)}
                  placeholder="ma-base"
                  className="w-full bg-surface border border-gray-200 rounded-xl px-3 py-2.5 text-sm text-text
                             focus:ring-2 focus:ring-primary/20 focus:border-primary/40 focus:outline-none transition-all"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-text-light mb-1">Login</label>
                <input
                  type="email"
                  value={login}
                  onChange={(e) => setLogin(e.target.value)}
                  placeholder="admin@monentreprise.com"
                  className="w-full bg-surface border border-gray-200 rounded-xl px-3 py-2.5 text-sm text-text
                             focus:ring-2 focus:ring-primary/20 focus:border-primary/40 focus:outline-none transition-all"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-text-light mb-1">Cle API</label>
                <input
                  type="password"
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  placeholder="Cle API Odoo"
                  className="w-full bg-surface border border-gray-200 rounded-xl px-3 py-2.5 text-sm text-text
                             focus:ring-2 focus:ring-primary/20 focus:border-primary/40 focus:outline-none transition-all"
                />
                <p className="text-[11px] text-text-muted mt-1">
                  Odoo &gt; Parametres &gt; Utilisateurs &gt; Cles API
                </p>
              </div>
            </div>

            <div className="flex gap-2 mt-5">
              <button
                onClick={() => setIsOpen(false)}
                className="flex-1 bg-surface text-text py-2.5 rounded-xl text-sm font-medium
                           hover:bg-surface-hover transition-all"
              >
                Annuler
              </button>
              <button
                onClick={handleSubmit}
                disabled={!url || !db || !login || !apiKey}
                className="flex-1 bg-primary text-white py-2.5 rounded-xl text-sm font-medium
                           hover:bg-primary-600 disabled:opacity-40 transition-all"
              >
                Connecter
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
