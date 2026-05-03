/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: {
          950: "#020403",
          900: "#050907",
          800: "#09120d",
          700: "#0d1d14",
        },
        neon: {
          green: "#23f58c",
          mint: "#b9ffd8",
          muted: "#66d99a",
        },
      },
      boxShadow: {
        glow: "0 0 42px rgba(35, 245, 140, 0.24)",
        soft: "0 20px 80px rgba(0, 0, 0, 0.4)",
      },
      fontFamily: {
        sans: [
          "Inter",
          "ui-sans-serif",
          "system-ui",
          "-apple-system",
          "BlinkMacSystemFont",
          "Segoe UI",
          "sans-serif",
        ],
        mono: [
          "JetBrains Mono",
          "SFMono-Regular",
          "Consolas",
          "Liberation Mono",
          "monospace",
        ],
      },
    },
  },
  plugins: [],
};
