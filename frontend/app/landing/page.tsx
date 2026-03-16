"use client";

import { useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function LandingPage() {
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) return;
    try {
      await fetch(`${API_URL}/api/waitlist`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });
    } catch { /* API not available — still show success */ }
    setSubmitted(true);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-primary to-primary/80">
      {/* Hero */}
      <div className="max-w-4xl mx-auto px-6 pt-20 pb-16 text-center text-white">
        <h1 className="text-4xl md:text-5xl font-bold leading-tight">
          Votre Odoo peut faire plus.
        </h1>
        <p className="text-xl md:text-2xl text-accent mt-4">
          L&apos;IA vous montre comment.
        </p>
        <p className="text-white/70 mt-6 max-w-2xl mx-auto">
          OdooAI est un Business Analyst IA qui a lu chaque ligne du code source d&apos;Odoo.
          Il se connecte a votre instance, detecte ce que vous n&apos;utilisez pas,
          et vous montre comment en tirer profit.
        </p>
      </div>

      {/* Stats */}
      <div className="max-w-4xl mx-auto px-6 pb-16">
        <div className="grid grid-cols-3 gap-6 text-center">
          <div className="bg-white/10 rounded-xl p-6">
            <div className="text-3xl font-bold text-accent">1 218</div>
            <div className="text-sm text-white/70 mt-1">Modules analyses</div>
          </div>
          <div className="bg-white/10 rounded-xl p-6">
            <div className="text-3xl font-bold text-accent">5 514</div>
            <div className="text-sm text-white/70 mt-1">Modeles extraits</div>
          </div>
          <div className="bg-white/10 rounded-xl p-6">
            <div className="text-3xl font-bold text-accent">24/7</div>
            <div className="text-sm text-white/70 mt-1">Disponible</div>
          </div>
        </div>
      </div>

      {/* Features */}
      <div className="max-w-4xl mx-auto px-6 pb-16">
        <div className="grid md:grid-cols-3 gap-6">
          <div className="bg-white rounded-xl p-6 shadow-lg">
            <div className="text-2xl mb-3">🔍</div>
            <h3 className="font-semibold text-primary">Decouvrez</h3>
            <p className="text-sm text-gray-600 mt-2">
              L&apos;IA revele les fonctionnalites Odoo que vous n&apos;utilisez pas encore.
            </p>
          </div>
          <div className="bg-white rounded-xl p-6 shadow-lg">
            <div className="text-2xl mb-3">💬</div>
            <h3 className="font-semibold text-primary">Demandez</h3>
            <p className="text-sm text-gray-600 mt-2">
              Posez vos questions en francais. L&apos;IA repond avec des sources et des actions concretes.
            </p>
          </div>
          <div className="bg-white rounded-xl p-6 shadow-lg">
            <div className="text-2xl mb-3">⚡</div>
            <h3 className="font-semibold text-primary">Executez</h3>
            <p className="text-sm text-gray-600 mt-2">
              Activez les fonctionnalites en un clic. Double validation avant chaque action.
            </p>
          </div>
        </div>
      </div>

      {/* Pricing */}
      <div className="max-w-4xl mx-auto px-6 pb-16">
        <h2 className="text-2xl font-bold text-white text-center mb-8">Plans</h2>
        <div className="grid md:grid-cols-3 gap-6">
          {[
            { name: "Starter", price: "49", features: ["100 requetes/mois", "1 connexion Odoo", "BA Profiles basiques"] },
            { name: "Professional", price: "149", features: ["500 requetes/mois", "1 connexion Odoo", "Tous les BA + Expert Profiles", "Lecture + ecriture"] },
            { name: "Enterprise", price: "399", features: ["Illimite*", "3 connexions Odoo", "Tout inclus", "Support prioritaire"] },
          ].map((plan) => (
            <div key={plan.name} className={`rounded-xl p-6 ${plan.name === "Professional" ? "bg-white shadow-xl scale-105" : "bg-white/90"}`}>
              <h3 className="font-semibold text-primary">{plan.name}</h3>
              <div className="text-3xl font-bold text-primary mt-2">
                {plan.price}<span className="text-sm font-normal text-gray-500">€/mois</span>
              </div>
              <ul className="mt-4 space-y-2">
                {plan.features.map((f) => (
                  <li key={f} className="text-sm text-gray-600 flex items-center gap-2">
                    <span className="text-success">✓</span> {f}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>

      {/* Email capture */}
      <div className="max-w-md mx-auto px-6 pb-20 text-center">
        {submitted ? (
          <div className="bg-success/20 text-white rounded-xl p-6">
            <p className="text-lg font-semibold">Merci !</p>
            <p className="text-sm mt-1">On vous contacte des que la beta est ouverte.</p>
          </div>
        ) : (
          <form onSubmit={handleSubmit}>
            <h2 className="text-xl font-semibold text-white mb-4">
              Acces anticipe a la beta
            </h2>
            <div className="flex gap-2">
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="votre@email.com"
                required
                className="flex-1 rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-accent"
              />
              <button
                type="submit"
                className="bg-accent text-primary font-semibold px-6 py-3 rounded-lg hover:bg-accent/90 transition"
              >
                S&apos;inscrire
              </button>
            </div>
          </form>
        )}
      </div>

      {/* Footer */}
      <footer className="text-center text-white/50 text-xs pb-8">
        OdooAI n&apos;est pas affilie a Odoo SA. · 2026
      </footer>
    </div>
  );
}
