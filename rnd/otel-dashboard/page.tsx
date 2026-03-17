"use client";

import { useState, useEffect, useCallback } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface Metrics {
  chat_requests_total: number;
  tokens_total: number;
  tool_calls_total: number;
  guardian_blocks_total: number;
  conversations_total: number;
  haiku_requests: number;
  sonnet_requests: number;
  latency_p50: number;
  latency_p95: number;
  latency_p99: number;
  latency_samples: number;
}

interface MetricCardProps {
  label: string;
  value: string | number;
  subtitle?: string;
  color: "purple" | "green" | "red" | "cyan";
}

function MetricCard({ label, value, subtitle, color }: MetricCardProps) {
  const colorMap = {
    purple: {
      bg: "bg-[#6C5CE7]/10",
      text: "text-[#6C5CE7]",
      border: "border-[#6C5CE7]/20",
    },
    green: {
      bg: "bg-emerald-50",
      text: "text-emerald-600",
      border: "border-emerald-200",
    },
    red: {
      bg: "bg-red-50",
      text: "text-red-500",
      border: "border-red-200",
    },
    cyan: {
      bg: "bg-[#00D2FF]/10",
      text: "text-[#00A3CC]",
      border: "border-[#00D2FF]/20",
    },
  };

  const c = colorMap[color];

  return (
    <div
      className={`${c.bg} border ${c.border} rounded-2xl p-5 flex flex-col gap-1 transition-all hover:shadow-md`}
    >
      <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">
        {label}
      </p>
      <p className={`text-3xl font-bold ${c.text} tracking-tight`}>
        {value}
      </p>
      {subtitle && (
        <p className="text-[11px] text-gray-400 mt-1">{subtitle}</p>
      )}
    </div>
  );
}

export default function OtelDashboardPage() {
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);
  const [secondsAgo, setSecondsAgo] = useState(0);
  const [error, setError] = useState<string | null>(null);

  const fetchMetrics = useCallback(async () => {
    try {
      const res = await fetch(`${API_URL}/metrics`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data: Metrics = await res.json();
      setMetrics(data);
      setLastUpdated(new Date());
      setSecondsAgo(0);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch metrics");
    }
  }, []);

  // Fetch every 5 seconds
  useEffect(() => {
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 5000);
    return () => clearInterval(interval);
  }, [fetchMetrics]);

  // Update "seconds ago" counter every second
  useEffect(() => {
    const tick = setInterval(() => {
      if (lastUpdated) {
        setSecondsAgo(Math.floor((Date.now() - lastUpdated.getTime()) / 1000));
      }
    }, 1000);
    return () => clearInterval(tick);
  }, [lastUpdated]);

  const formatNumber = (n: number): string => {
    if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
    if (n >= 1_000) return `${(n / 1_000).toFixed(1)}K`;
    return n.toLocaleString();
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-100 px-6 py-4">
        <div className="max-w-5xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 bg-[#6C5CE7] rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-[10px]">AI</span>
            </div>
            <div>
              <h1 className="text-sm font-semibold text-gray-900">
                OdooAI Observability
              </h1>
              <p className="text-[11px] text-gray-400">
                Real-time metrics dashboard
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <span
              className={`inline-block w-2 h-2 rounded-full ${
                error ? "bg-red-400" : "bg-emerald-400 animate-pulse"
              }`}
            />
            <span className="text-xs text-gray-400">
              {error
                ? "Disconnected"
                : lastUpdated
                  ? `Updated ${secondsAgo}s ago`
                  : "Connecting..."}
            </span>
          </div>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-6 py-8">
        {/* Error banner */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-xl px-4 py-3 mb-6 text-sm text-red-600">
            Cannot reach {API_URL}/metrics — {error}
          </div>
        )}

        {/* Primary metrics */}
        <section className="mb-8">
          <h2 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">
            Usage
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            <MetricCard
              label="Chat Requests"
              value={metrics ? formatNumber(metrics.chat_requests_total) : "—"}
              subtitle="Total requests processed"
              color="purple"
            />
            <MetricCard
              label="Tokens"
              value={metrics ? formatNumber(metrics.tokens_total) : "—"}
              subtitle="Total tokens consumed"
              color="purple"
            />
            <MetricCard
              label="Tool Calls"
              value={metrics ? formatNumber(metrics.tool_calls_total) : "—"}
              subtitle="Odoo tool invocations"
              color="cyan"
            />
            <MetricCard
              label="Conversations"
              value={
                metrics ? formatNumber(metrics.conversations_total) : "—"
              }
              subtitle="Active conversation threads"
              color="purple"
            />
            <MetricCard
              label="Guardian Blocks"
              value={
                metrics ? formatNumber(metrics.guardian_blocks_total) : "—"
              }
              subtitle="Security blocks triggered"
              color="red"
            />
          </div>
        </section>

        {/* Model breakdown */}
        <section className="mb-8">
          <h2 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">
            Model Breakdown
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            <MetricCard
              label="Haiku Requests"
              value={metrics ? formatNumber(metrics.haiku_requests) : "—"}
              subtitle="Fast / low-cost model"
              color="cyan"
            />
            <MetricCard
              label="Sonnet Requests"
              value={metrics ? formatNumber(metrics.sonnet_requests) : "—"}
              subtitle="Balanced model"
              color="purple"
            />
            {metrics && metrics.chat_requests_total > 0 && (
              <MetricCard
                label="Haiku Ratio"
                value={`${Math.round((metrics.haiku_requests / metrics.chat_requests_total) * 100)}%`}
                subtitle="Cost optimization indicator"
                color="green"
              />
            )}
          </div>
        </section>

        {/* Latency metrics */}
        <section>
          <h2 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">
            Latency
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            <MetricCard
              label="P50 Latency"
              value={metrics ? `${metrics.latency_p50.toFixed(1)}s` : "—"}
              subtitle="Median response time"
              color="green"
            />
            <MetricCard
              label="P95 Latency"
              value={metrics ? `${metrics.latency_p95.toFixed(1)}s` : "—"}
              subtitle="95th percentile"
              color="green"
            />
            <MetricCard
              label="P99 Latency"
              value={metrics ? `${metrics.latency_p99.toFixed(1)}s` : "—"}
              subtitle={
                metrics
                  ? `Based on ${metrics.latency_samples} samples`
                  : "99th percentile"
              }
              color={
                metrics && metrics.latency_p99 > 15 ? "red" : "green"
              }
            />
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="text-center py-4 text-[11px] text-gray-300">
        OdooAI Observability — R&amp;D Agent 38
      </footer>
    </div>
  );
}
