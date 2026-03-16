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
        <span className="text-xs text-green-300">● Connecte</span>
        <button
          onClick={onDisconnect}
          className="text-xs text-white/70 hover:text-white underline"
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
        className="text-xs bg-white/20 text-white px-3 py-1 rounded hover:bg-white/30 transition"
      >
        Connecter Odoo
      </button>

      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
          <div className="bg-white rounded-xl shadow-xl p-6 w-full max-w-md mx-4">
            <h3 className="text-lg font-semibold text-primary mb-4">
              Connexion a votre Odoo
            </h3>

            <div className="space-y-3">
              <div>
                <label className="block text-sm text-gray-600 mb-1">URL instance</label>
                <input
                  type="url"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  placeholder="https://mon-odoo.com ou http://localhost:8069"
                  className="w-full border rounded-lg px-3 py-2 text-sm text-gray-900 focus:ring-2 focus:ring-primary focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-sm text-gray-600 mb-1">Base de donnees</label>
                <input
                  type="text"
                  value={db}
                  onChange={(e) => setDb(e.target.value)}
                  placeholder="ma-base"
                  className="w-full border rounded-lg px-3 py-2 text-sm text-gray-900 focus:ring-2 focus:ring-primary focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-sm text-gray-600 mb-1">Login</label>
                <input
                  type="email"
                  value={login}
                  onChange={(e) => setLogin(e.target.value)}
                  placeholder="admin@monentreprise.com"
                  className="w-full border rounded-lg px-3 py-2 text-sm text-gray-900 focus:ring-2 focus:ring-primary focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-sm text-gray-600 mb-1">Cle API</label>
                <input
                  type="password"
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  placeholder="Votre cle API Odoo"
                  className="w-full border rounded-lg px-3 py-2 text-sm text-gray-900 focus:ring-2 focus:ring-primary focus:outline-none"
                />
                <p className="text-xs text-gray-400 mt-1">
                  Odoo &gt; Parametres &gt; Utilisateurs &gt; Cles API
                </p>
              </div>
            </div>

            <div className="flex gap-2 mt-5">
              <button
                onClick={() => setIsOpen(false)}
                className="flex-1 border border-gray-300 text-gray-600 py-2 rounded-lg text-sm hover:bg-gray-50"
              >
                Annuler
              </button>
              <button
                onClick={handleSubmit}
                disabled={!url || !db || !login || !apiKey}
                className="flex-1 bg-primary text-white py-2 rounded-lg text-sm hover:bg-primary/90 disabled:opacity-50"
              >
                Connecter
              </button>
            </div>

            <p className="text-xs text-gray-400 text-center mt-3">
              🔒 Vos identifiants ne sont pas stockes — session uniquement.
            </p>
          </div>
        </div>
      )}
    </>
  );
}
