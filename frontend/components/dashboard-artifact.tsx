"use client";

import { useEffect, useState } from "react";

interface KPIData {
  label: string;
  value: number;
  icon?: string;
  format?: string; // "currency", "percent", "number"
  trend?: string; // "+12%", "-3"
  color?: string; // "red", "green", "blue", "purple", "amber"
}

interface BarData {
  label: string;
  value: number;
  max: number;
  color?: string;
}

interface DashboardData {
  title?: string;
  kpis?: KPIData[];
  bars?: BarData[];
  alerts?: string[];
}

const COLOR_MAP: Record<string, string> = {
  red: "bg-red-50 text-red-700 border-red-200",
  green: "bg-green-50 text-green-700 border-green-200",
  blue: "bg-blue-50 text-blue-700 border-blue-200",
  purple: "bg-purple-50 text-purple-700 border-purple-200",
  amber: "bg-amber-50 text-amber-700 border-amber-200",
};

const BAR_COLORS: Record<string, string> = {
  red: "bg-red-500",
  green: "bg-green-500",
  blue: "bg-blue-500",
  purple: "bg-purple-500",
  amber: "bg-amber-500",
};

function AnimatedNumber({ value, format }: { value: number; format?: string }) {
  const [display, setDisplay] = useState(0);

  useEffect(() => {
    const duration = 1000;
    const steps = 30;
    const increment = value / steps;
    let current = 0;
    const timer = setInterval(() => {
      current += increment;
      if (current >= value) {
        setDisplay(value);
        clearInterval(timer);
      } else {
        setDisplay(Math.round(current));
      }
    }, duration / steps);
    return () => clearInterval(timer);
  }, [value]);

  if (format === "currency") {
    return <>{display.toLocaleString("fr-FR")}€</>;
  }
  if (format === "percent") {
    return <>{display}%</>;
  }
  return <>{display.toLocaleString("fr-FR")}</>;
}

function AnimatedBar({ value, max, color }: { value: number; max: number; color?: string }) {
  const [width, setWidth] = useState(0);
  const percent = Math.round((value / max) * 100);

  useEffect(() => {
    const timer = setTimeout(() => setWidth(percent), 100);
    return () => clearTimeout(timer);
  }, [percent]);

  const barColor = BAR_COLORS[color || "blue"] || "bg-primary";

  return (
    <div className="flex items-center gap-3">
      <div className="flex-1 bg-gray-100 rounded-full h-2.5 overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-1000 ease-out ${barColor}`}
          style={{ width: `${width}%` }}
        />
      </div>
      <span className="text-xs font-medium text-text-muted w-10 text-right">{percent}%</span>
    </div>
  );
}

export function DashboardArtifact({ data }: { data: DashboardData }) {
  return (
    <div className="my-3 rounded-xl border border-gray-200 overflow-hidden animate-fadeIn">
      {/* Header */}
      {data.title && (
        <div className="bg-gradient-to-r from-primary to-primary-600 px-4 py-3">
          <h3 className="text-sm font-semibold text-white">{data.title}</h3>
        </div>
      )}

      <div className="p-4 space-y-4">
        {/* KPI Cards */}
        {data.kpis && data.kpis.length > 0 && (
          <div className={`grid gap-3 ${
            data.kpis.length <= 2 ? "grid-cols-2" :
            data.kpis.length <= 3 ? "grid-cols-3" : "grid-cols-2 md:grid-cols-4"
          }`}>
            {data.kpis.map((kpi, i) => {
              const colorClass = COLOR_MAP[kpi.color || "blue"] || COLOR_MAP.blue;
              return (
                <div
                  key={i}
                  className={`rounded-lg border p-3 ${colorClass} animate-fadeIn`}
                  style={{ animationDelay: `${i * 100}ms` }}
                >
                  <div className="flex items-center justify-between">
                    {kpi.icon && <span className="text-lg">{kpi.icon}</span>}
                    {kpi.trend && (
                      <span className={`text-[10px] font-medium px-1.5 py-0.5 rounded-full ${
                        kpi.trend.startsWith("+") ? "bg-green-100 text-green-700" :
                        kpi.trend.startsWith("-") ? "bg-red-100 text-red-700" : "bg-gray-100 text-gray-600"
                      }`}>
                        {kpi.trend}
                      </span>
                    )}
                  </div>
                  <p className="text-xl font-bold mt-1">
                    <AnimatedNumber value={kpi.value} format={kpi.format} />
                  </p>
                  <p className="text-xs font-medium opacity-70 mt-0.5">{kpi.label}</p>
                </div>
              );
            })}
          </div>
        )}

        {/* Progress Bars */}
        {data.bars && data.bars.length > 0 && (
          <div className="space-y-3">
            {data.bars.map((bar, i) => (
              <div key={i}>
                <div className="flex justify-between text-xs mb-1">
                  <span className="font-medium text-text">{bar.label}</span>
                  <span className="text-text-muted">{bar.value}/{bar.max}</span>
                </div>
                <AnimatedBar value={bar.value} max={bar.max} color={bar.color} />
              </div>
            ))}
          </div>
        )}

        {/* Alerts */}
        {data.alerts && data.alerts.length > 0 && (
          <div className="space-y-1.5">
            {data.alerts.map((alert, i) => (
              <div key={i} className="flex items-center gap-2 text-xs text-amber-700 bg-amber-50 px-3 py-2 rounded-lg">
                <span>⚠️</span>
                <span>{alert}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export function tryParseDashboard(text: string): { before: string; dashboard: DashboardData | null; after: string } {
  const dashboardRegex = /```dashboard\s*\n([\s\S]*?)```/;
  const match = text.match(dashboardRegex);

  if (!match) {
    return { before: text, dashboard: null, after: "" };
  }

  try {
    const data = JSON.parse(match[1]) as DashboardData;
    const idx = match.index || 0;
    const before = text.slice(0, idx).trim();
    const after = text.slice(idx + match[0].length).trim();
    return { before, dashboard: data, after };
  } catch {
    return { before: text, dashboard: null, after: "" };
  }
}
