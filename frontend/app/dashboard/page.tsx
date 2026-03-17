"use client";

import { useState, useEffect } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface KPI {
  label: string;
  value: string;
  detail: string;
  color: string;
  icon: string;
}

interface DashboardData {
  kpis: KPI[];
  loading: boolean;
  connected: boolean;
  error: string;
}

export default function DashboardPage() {
  const [data, setData] = useState<DashboardData>({
    kpis: [],
    loading: true,
    connected: false,
    error: "",
  });

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      // Check if we have a saved connection
      const connRes = await fetch(`${API_URL}/api/connections`);
      if (!connRes.ok) {
        setData({ kpis: [], loading: false, connected: false, error: "" });
        return;
      }
      const connections = await connRes.json();
      if (connections.length === 0) {
        setData({ kpis: [], loading: false, connected: false, error: "" });
        return;
      }

      const conn = connections[0];

      // Fetch KPIs via chat API with a special dashboard query
      const chatRes = await fetch(`${API_URL}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: "Donne-moi un resume dashboard : nombre de devis en brouillon, commandes confirmees ce mois, factures impayees, et transferts en attente. Reponds UNIQUEMENT avec des chiffres, pas d'explication.",
          odoo_url: conn.url,
          odoo_db: conn.db_name,
          odoo_login: conn.login,
          odoo_api_key: `connection:${conn.id}`,
        }),
      });

      if (!chatRes.ok) {
        setData({ kpis: [], loading: false, connected: true, error: "Erreur API" });
        return;
      }

      // Parse SSE response
      const reader = chatRes.body?.getReader();
      if (!reader) return;
      const decoder = new TextDecoder();
      let fullText = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value);
        for (const line of chunk.split("\n")) {
          if (!line.startsWith("data: ")) continue;
          try {
            const d = JSON.parse(line.slice(6));
            if (d.type === "text") fullText += d.content;
          } catch { /* skip */ }
        }
      }

      // Parse the response into KPIs (best effort)
      const kpis = parseKPIs(fullText);
      setData({ kpis, loading: false, connected: true, error: "" });
    } catch (err) {
      setData({ kpis: [], loading: false, connected: false, error: "Connexion impossible" });
    }
  };

  return (
    <div className="min-h-screen bg-surface p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold text-text">Dashboard OdooAI</h1>
            <p className="text-sm text-text-muted mt-1">
              {data.connected ? "Connecte a votre Odoo" : "Connectez votre Odoo pour voir vos KPIs"}
            </p>
          </div>
          <div className="flex items-center gap-3">
            {data.connected && (
              <div className="flex items-center gap-1.5 bg-green-50 px-2.5 py-1 rounded-lg">
                <div className="w-2 h-2 bg-success rounded-full" />
                <span className="text-xs text-success font-medium">Connecte</span>
              </div>
            )}
            <button
              onClick={loadDashboard}
              className="text-xs bg-primary/10 text-primary font-medium px-3 py-1.5 rounded-lg hover:bg-primary/20 transition-all"
            >
              Rafraichir
            </button>
            <a
              href="/"
              className="text-xs bg-primary text-white font-medium px-3 py-1.5 rounded-lg hover:bg-primary-600 transition-all"
            >
              Chat
            </a>
          </div>
        </div>

        {/* Loading */}
        {data.loading && (
          <div className="flex items-center justify-center py-20">
            <div className="w-8 h-8 border-3 border-primary/30 border-t-primary rounded-full animate-spin" />
            <span className="ml-3 text-text-muted">Chargement des KPIs...</span>
          </div>
        )}

        {/* Not connected */}
        {!data.loading && !data.connected && (
          <div className="text-center py-20">
            <div className="w-16 h-16 bg-primary/10 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <span className="text-3xl">📊</span>
            </div>
            <h2 className="text-lg font-semibold text-text">Connectez votre Odoo</h2>
            <p className="text-sm text-text-muted mt-2">
              Allez dans le <a href="/" className="text-primary underline">chat</a> et connectez votre instance Odoo pour voir vos KPIs.
            </p>
          </div>
        )}

        {/* KPIs from AI response */}
        {!data.loading && data.connected && (
          <div className="bg-white rounded-2xl shadow-card p-6">
            <h2 className="text-sm font-semibold text-text mb-4">Resume de votre Odoo</h2>
            <div className="prose prose-sm max-w-none text-text whitespace-pre-wrap">
              {data.kpis.length > 0 ? (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {data.kpis.map((kpi, i) => (
                    <div key={i} className={`rounded-xl p-4 ${kpi.color}`}>
                      <span className="text-2xl">{kpi.icon}</span>
                      <p className="text-2xl font-bold mt-2">{kpi.value}</p>
                      <p className="text-sm font-medium mt-1">{kpi.label}</p>
                      {kpi.detail && <p className="text-xs opacity-70 mt-0.5">{kpi.detail}</p>}
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-text-muted">Les KPIs seront affiches ici apres analyse.</p>
              )}
            </div>
          </div>
        )}

        {/* Quick actions */}
        {!data.loading && data.connected && (
          <div className="mt-6 grid grid-cols-2 md:grid-cols-4 gap-3">
            {[
              { emoji: "📋", text: "Commandes en retard", href: "/?q=Mes commandes en retard ?" },
              { emoji: "💰", text: "Factures impayees", href: "/?q=Factures impayees avec montants" },
              { emoji: "📦", text: "Stock critique", href: "/?q=Produits en rupture de stock" },
              { emoji: "📊", text: "CA du mois", href: "/?q=Mon chiffre d affaires ce mois" },
            ].map((action) => (
              <a
                key={action.text}
                href={action.href}
                className="bg-white border border-gray-200 rounded-xl px-4 py-3 text-left hover:border-primary/30 hover:shadow-soft transition-all group"
              >
                <span className="text-lg">{action.emoji}</span>
                <p className="text-xs font-medium text-text mt-1 group-hover:text-primary transition-colors">
                  {action.text}
                </p>
              </a>
            ))}
          </div>
        )}

        {/* System metrics */}
        <div className="mt-6">
          <SystemMetrics />
        </div>
      </div>
    </div>
  );
}

function SystemMetrics() {
  const [metrics, setMetrics] = useState<Record<string, number>>({});

  useEffect(() => {
    const load = async () => {
      try {
        const res = await fetch(`${API_URL}/metrics`);
        if (res.ok) setMetrics(await res.json());
      } catch { /* ignore */ }
    };
    load();
    const interval = setInterval(load, 10000);
    return () => clearInterval(interval);
  }, []);

  if (Object.keys(metrics).length === 0) return null;

  return (
    <div className="bg-white rounded-2xl shadow-card p-6">
      <h2 className="text-sm font-semibold text-text mb-4">Metriques systeme</h2>
      <div className="grid grid-cols-3 md:grid-cols-6 gap-3">
        {[
          { key: "chat_requests_total", label: "Requetes", icon: "💬" },
          { key: "tokens_total", label: "Tokens", icon: "🔤" },
          { key: "tool_calls_total", label: "Tool calls", icon: "🔧" },
          { key: "latency_p50", label: "Latence p50", icon: "⚡", suffix: "s" },
          { key: "latency_p95", label: "Latence p95", icon: "📈", suffix: "s" },
          { key: "conversations_total", label: "Conversations", icon: "📂" },
        ].map((m) => (
          <div key={m.key} className="text-center p-3 rounded-lg bg-surface">
            <span className="text-lg">{m.icon}</span>
            <p className="text-lg font-bold text-text mt-1">
              {metrics[m.key] !== undefined
                ? `${typeof metrics[m.key] === "number" && metrics[m.key] > 1000
                    ? `${(metrics[m.key] / 1000).toFixed(1)}K`
                    : metrics[m.key]}${m.suffix || ""}`
                : "-"}
            </p>
            <p className="text-[10px] text-text-muted">{m.label}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

function parseKPIs(text: string): KPI[] {
  // Best-effort parsing of LLM response into KPI cards
  const kpis: KPI[] = [];
  const patterns = [
    { regex: /(\d+)\s*devis/i, label: "Devis en brouillon", icon: "📝", color: "bg-blue-50 text-blue-800" },
    { regex: /(\d+)\s*commande/i, label: "Commandes confirmees", icon: "✅", color: "bg-green-50 text-green-800" },
    { regex: /(\d+)\s*facture/i, label: "Factures impayees", icon: "💰", color: "bg-amber-50 text-amber-800" },
    { regex: /(\d+)\s*transfert/i, label: "Transferts en attente", icon: "📦", color: "bg-purple-50 text-purple-800" },
  ];

  for (const p of patterns) {
    const match = text.match(p.regex);
    if (match) {
      kpis.push({
        value: match[1],
        label: p.label,
        detail: "",
        icon: p.icon,
        color: p.color,
      });
    }
  }

  // If no patterns matched, try to extract any numbers with context
  if (kpis.length === 0) {
    const lines = text.split("\n").filter((l) => l.trim());
    for (const line of lines.slice(0, 4)) {
      const numMatch = line.match(/\*?\*?(\d[\d\s,.]*)\*?\*?/);
      if (numMatch) {
        kpis.push({
          value: numMatch[1].trim(),
          label: line.replace(numMatch[0], "").replace(/[*#|-]/g, "").trim().slice(0, 40),
          detail: "",
          icon: "📊",
          color: "bg-gray-50 text-gray-800",
        });
      }
    }
  }

  return kpis;
}
