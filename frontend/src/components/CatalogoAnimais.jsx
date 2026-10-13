import React, { useState, useEffect, useCallback } from 'react';
import { buscarCatalogo } from '../services/animalService';
import { AnimalCard } from '../components/AnimalCard';
import { FiltrosCatalogo } from '../components/FiltrosCatalogo';
import { Button } from '../components/Button';

// Os estados explícitos protegem a UI de apresentar dados inconsistentes
const ESTADOS_TELA = {
  CARREGANDO: 'CARREGANDO',
  SUCESSO: 'SUCESSO',
  ERRO: 'ERRO',
  VAZIO: 'VAZIO'
};

export const CatalogoAnimais = () => {
  const [animais, setAnimais] = useState([]);
  const [estadoTela, setEstadoTela] = useState(ESTADOS_TELA.CARREGANDO);
  const [mensagemErro, setMensagemErro] = useState('');

  // A função é memorizada para evitar re-renderizações desnecessárias ao ser passada como prop
  const carregarDados = useCallback(async (filtros = {}) => {
    setEstadoTela(ESTADOS_TELA.CARREGANDO);
    try {
      // Consome o Use Case "BuscarCatalogo" mapeado no service
      const resultado = await buscarCatalogo(filtros);
      
      if (!resultado || resultado.length === 0) {
        setEstadoTela(ESTADOS_TELA.VAZIO);
      } else {
        setAnimais(resultado);
        setEstadoTela(ESTADOS_TELA.SUCESSO);
      }
    } catch (erro) {
      setMensagemErro(erro.message || 'Ocorreu um erro ao carregar o catálogo.');
      setEstadoTela(ESTADOS_TELA.ERRO);
    }
  }, []);

  // Carregamento inicial do catálogo (sem filtros)
  useEffect(() => {
    carregarDados();
  }, [carregarDados]);

  const handleNavegarParaAnimal = (id) => {
    // Aqui integraria com o React Router para a página de detalhes/solicitação
    console.log(`Navegar para detalhes do animal: ${id}`);
  };

  // Máquina de Estados UI/UX: Renderização condicional baseada no estado atual da transação
  const renderizarConteudo = () => {
    switch (estadoTela) {
      case ESTADOS_TELA.CARREGANDO:
        // Feedback visual imediato durante o fetching de dados
        return (
          <div className="flex justify-center items-center py-20" aria-live="polite">
            <span className="w-10 h-10 border-4 border-primaria border-t-transparent rounded-full animate-spin" />
            <span className="sr-only">Carregando catálogo...</span>
          </div>
        );

      case ESTADOS_TELA.ERRO:
        // Hierarquia Visual: Centralização e uso da cor semântica de erro para atrair a atenção à falha
        return (
          <div className="text-center py-16 bg-white rounded-xl border border-borda">
            <h2 className="text-xl font-bold text-erro mb-2">Ops! Algo deu errado.</h2>
            <p className="text-textoCorpo mb-6">{mensagemErro}</p>
            <div className="max-w-xs mx-auto">
              <Button onClick={() => carregarDados()} variante="secundaria" fullWidth>
                Tentar novamente
              </Button>
            </div>
          </div>
        );

      case ESTADOS_TELA.VAZIO:
        // Prevenção de "tela em branco" quando a busca não retorna resultados
        return (
          <div className="text-center py-16 bg-white rounded-xl border border-borda">
            <h2 className="text-xl font-bold text-textoDestaque mb-2">Nenhum animal encontrado</h2>
            <p className="text-textoApoio">Tente ajustar seus filtros para encontrar o que procura.</p>
          </div>
        );

      case ESTADOS_TELA.SUCESSO:
        // Mobile First: Grid responsivo de 1 coluna (mobile) até 3 colunas (desktop)
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
        
        {/* Hierarquia Visual: Título da página é o maior elemento textual (h1) */}
        <header className="mb-8">
          <h1 className="text-3xl font-black text-textoDestaque tracking-tight">
            Animais para Adoção
          </h1>
          <p className="text-textoCorpo mt-2">
            Conheça nossos resgatados e encontre seu novo melhor amigo.
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