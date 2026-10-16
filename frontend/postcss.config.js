// Conecta o novo pacote do Tailwind v4 ao pipeline de estilos do Vite para permitir a compilação da UI
export default {
  plugins: {
    '@tailwindcss/postcss': {},
    autoprefixer: {},
  },
}