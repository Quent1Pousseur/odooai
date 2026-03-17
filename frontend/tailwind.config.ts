import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "#6C5CE7",
          50: "#F3F1FE",
          100: "#E8E4FD",
          200: "#D1C9FB",
          300: "#B0A3F8",
          400: "#8F7CF5",
          500: "#6C5CE7",
          600: "#5A48D5",
          700: "#4836B3",
          800: "#362A8A",
          900: "#251D61",
        },
        accent: {
          DEFAULT: "#00D2FF",
          50: "#E6FAFF",
          100: "#B3F0FF",
          200: "#80E6FF",
          300: "#4DDBFF",
          400: "#1AD1FF",
          500: "#00D2FF",
          600: "#00A8CC",
        },
        surface: {
          DEFAULT: "#F8F9FC",
          card: "#FFFFFF",
          hover: "#F1F3F9",
          sidebar: "#1E1E2E",
        },
        text: {
          DEFAULT: "#2D3748",
          light: "#718096",
          muted: "#A0AEC0",
        },
        success: "#48BB78",
        warning: "#ECC94B",
        danger: "#FC8181",
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      borderRadius: {
        "2xl": "1rem",
        "3xl": "1.5rem",
      },
      boxShadow: {
        "soft": "0 2px 15px rgba(0,0,0,0.04)",
        "card": "0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04)",
      },
    },
  },
  plugins: [],
};

export default config;
