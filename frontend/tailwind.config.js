/** @type {import('tailwindcss').Config} */
// Uso de export default para manter compatibilidade estrita com ES Modules no Vite
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      // Centralização dos tokens de cor do projeto para evitar valores hexadecimais soltos nos componentes
      colors: {
        primaria: "#84CC16", 
        secundaria: "#73C2FB", 
        fundo: "#F4F7F4", 
        sucesso: "#10B981",
        erro: "#EF4444",
        alerta: "#F59E0B",
        textoDestaque: "#1A2E1A",
        textoCorpo: "#3F4A3F",
        textoApoio: "#6B7262",
        borda: "#D1D5DB"
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}