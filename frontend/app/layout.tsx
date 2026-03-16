import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "OdooAI — Votre Odoo peut faire plus",
  description:
    "Business Analyst IA qui a lu chaque ligne du code source Odoo. Decouvrez les fonctionnalites que vous n'utilisez pas.",
  manifest: "/manifest.json",
  themeColor: "#1B2A4A",
  openGraph: {
    title: "OdooAI — Votre Odoo peut faire plus",
    description:
      "1218 modules analyses. 5514 modeles. L'IA qui connait Odoo mieux que vous.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fr">
      <head>
        {/* Plausible Analytics — privacy-first, no cookies (S5-27) */}
        {process.env.NEXT_PUBLIC_PLAUSIBLE_DOMAIN && (
          <script
            defer
            data-domain={process.env.NEXT_PUBLIC_PLAUSIBLE_DOMAIN}
            src="https://plausible.io/js/script.js"
          />
        )}
      </head>
      <body>{children}</body>
    </html>
  );
}
