import React from "react";
import { BrowserRouter as Router, Routes, Route, NavLink } from "react-router-dom";
import { CatalogoAnimais } from "./pages/CatalogoAnimais";
import { CadastroAnimal } from "./pages/CadastroAnimal";
import { FormularioAdocao } from "./pages/FormularioAdocao";
import { PainelAvaliacao } from "./pages/PainelAvaliacao";

export const App = () => {
  // Affordance e Hierarquia Visual: diferencia claramente a rota ativa das demais opções de navegação.
  const obterClasseLink = ({ isActive }) =>
    `px-4 py-2 rounded-lg font-medium transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-secundaria ${
      isActive
        ? "bg-primaria text-textoDestaque font-bold shadow-sm"
        : "text-textoCorpo hover:bg-fundo hover:text-textoDestaque"
    }`;

  return (
    <Router>
      <div className="min-h-screen flex flex-col bg-fundo font-sans text-textoCorpo">
        {/* Lei da Proximidade: barra superior agrupa a identidade da marca à esquerda e a navegação à direita, 
            separada do conteúdo da página por uma borda estrutural */}
        <header className="bg-white border-b border-borda sticky top-0 z-10">
          <nav
            className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between"
            aria-label="Navegacao principal"
          >
            <NavLink
              to="/"
              className="text-2xl font-black text-textoDestaque tracking-tight focus:outline-none focus:ring-2 focus:ring-primaria rounded"
            >
              MatchPet
            </NavLink>

            <div className="flex items-center gap-2">
              <NavLink to="/" end className={obterClasseLink}>
                Catalogo
              </NavLink>
              <NavLink to="/cadastro" className={obterClasseLink}>
                Registrar
              </NavLink>
              <NavLink to="/painel" className={obterClasseLink}>
                Painel
              </NavLink>
            </div>
          </nav>
        </header>

        <div className="flex-1">
          <Routes>
            <Route path="/" element={<CatalogoAnimais />} />
            <Route path="/cadastro" element={<CadastroAnimal />} />
            <Route path="/adocao/:animalId" element={<FormularioAdocao />} />
            <Route path="/painel" element={<PainelAvaliacao />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
};

export default App;