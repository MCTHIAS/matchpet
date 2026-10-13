/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Cores de marca definidas
        primaria: "#84CC16", 
        secundaria: "#73C2FB", 
        fundo: "#F4F7F4", 
        
        // Cores semânticas adaptadas para harmonizar com tons frios e vibrantes
        sucesso: "#10B981",
        erro: "#EF4444",
        alerta: "#F59E0B",
        
        // Escala neutra para hierarquia tipográfica (textos e bordas)
        textoDestaque: "#1A2E1A",
        textoCorpo: "#3F4A3F",
        textoApoio: "#6B7262",
        borda: "#D1D5DB"
      },
      fontFamily: {
        // Escala tipográfica única (Hierarquia Visual)
        sans: ['Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}