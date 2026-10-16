import React, { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { buscarCatalogo } from "../services/animalService";
import { AnimalCard } from "../components/AnimalCard";
import { FiltrosCatalogo } from "../components/FiltrosCatalogo";
import { Button } from "../components/Button";

// Máquina de Estados explícita para impedir renderização de listas vazias ou quebradas durante o fetch.
const ESTADOS_TELA = {
  CARREGANDO: "CARREGANDO",
  SUCESSO: "SUCESSO",
  ERRO: "ERRO",
  VAZIO: "VAZIO",
};

export const CatalogoAnimais = () => {
  const [animais, setAnimais] = useState([]);
  const [estadoTela, setEstadoTela] = useState(ESTADOS_TELA.CARREGANDO);
  const [mensagemErro, setMensagemErro] = useState("");

  const navigate = useNavigate();

  const carregarDados = useCallback(async (filtros = {}) => {
    setEstadoTela(ESTADOS_TELA.CARREGANDO);
    setMensagemErro("");

    try {
      const resultado = await buscarCatalogo(filtros);
      const lista = Array.isArray(resultado)
        ? resultado
        : resultado?.animais || resultado?.itens || [];

      if (lista.length === 0) {
        setAnimais([]);
        setEstadoTela(ESTADOS_TELA.VAZIO);
      } else {
        setAnimais(lista);
        setEstadoTela(ESTADOS_TELA.SUCESSO);
      }
    } catch (erro) {
      setMensagemErro(erro.message || "Ocorreu um erro ao carregar o catalogo.");
      setEstadoTela(ESTADOS_TELA.ERRO);
    }
  }, []);

  useEffect(() => {
    carregarDados();
  }, [carregarDados]);

  const handleNavegarParaAnimal = (id) => {
    navigate(`/adocao/${id}`);
  };

  const renderizarConteudo = () => {
    switch (estadoTela) {
      case ESTADOS_TELA.CARREGANDO:
        return (
          <div className="flex justify-center items-center py-20" aria-live="polite">
            <span className="w-10 h-10 border-4 border-primaria border-t-transparent rounded-full animate-spin" />
            <span className="sr-only">Carregando catalogo...</span>
          </div>
        );

      case ESTADOS_TELA.ERRO:
        return (
          <div className="text-center py-16 px-4 bg-white rounded-xl border border-borda">
            <h2 className="text-xl font-bold text-erro mb-2">
              Nao foi possivel carregar o catalogo
            </h2>
            <p className="text-textoCorpo mb-6">{mensagemErro}</p>
            <div className="max-w-xs mx-auto">
              <Button onClick={() => carregarDados()} variante="secundaria" fullWidth>
                Tentar novamente
              </Button>
            </div>
          </div>
        );

      case ESTADOS_TELA.VAZIO:
        return (
          <div className="text-center py-16 px-4 bg-white rounded-xl border border-borda">
            <h2 className="text-xl font-bold text-textoDestaque mb-2">
              Nenhum animal encontrado
            </h2>
            <p className="text-textoApoio">
              Tente ajustar seus filtros para encontrar o que procura.
            </p>
          </div>
        );

      case ESTADOS_TELA.SUCESSO:
        return (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
            {animais.map((animal) => (
              <AnimalCard
                key={animal.id}
                animal={animal}
                onClickAction={handleNavegarParaAnimal}
              />
            ))}
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <main className="min-h-screen bg-fundo px-4 py-8 md:py-12">
      <div className="max-w-6xl mx-auto">
        {/* Hierarquia Visual: título em destaque máximo conduz o olhar antes dos controles de filtro */}
        <header className="mb-8">
          <h1 className="text-3xl font-black text-textoDestaque tracking-tight">
            Animais para Adocao
          </h1>
          <p className="text-textoCorpo mt-2">
            Conheca nossos resgatados e encontre seu novo melhor amigo.
          </p>
        </header>

        <section aria-label="Filtros de busca">
          <FiltrosCatalogo
            onFiltrar={carregarDados}
            isLoading={estadoTela === ESTADOS_TELA.CARREGANDO}
          />
        </section>

        <section aria-label="Lista de animais" className="mt-8">
          {renderizarConteudo()}
        </section>
      </div>
    </main>
  );
};