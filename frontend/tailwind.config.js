export default {
  darkMode: ["class"], content: ['./src/**/*.{ts,tsx,vue}'],
  theme: { extend: { colors: { border: "hsl(var(--border))", background: "hsl(var(--background))", foreground: "hsl(var(--foreground))", primary: { DEFAULT: "hsl(var(--primary))", foreground: "hsl(var(--primary-foreground))" } } } },
  plugins: [require("tailwindcss-animate")]
}
