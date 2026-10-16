import React, { useState, useEffect, useCallback } from "react";
import {
  listarSolicitacoesPendentes,
  avaliarSolicitacao,
} from "../services/adocaoService";
import { Button } from "../components/Button";

const ESTADOS_PAINEL = {
  CARREGANDO: "CARREGANDO",
  SUCESSO: "SUCESSO",
  ERRO: "ERRO",
  VAZIO: "VAZIO",
};

export const PainelAvaliacao = () => {
  const [solicitacoes, setSolicitacoes] = useState([]);
  const [estadoPainel, setEstadoPainel] = useState(ESTADOS_PAINEL.CARREGANDO);
  const [mensagemErro, setMensagemErro] = useState("");
  const [erroAcao, setErroAcao] = useState("");
  const [processandoId, setProcessandoId] = useState(null);

  const carregarSolicitacoes = useCallback(async () => {
    setEstadoPainel(ESTADOS_PAINEL.CARREGANDO);
    setMensagemErro("");

    try {
      const resultado = await listarSolicitacoesPendentes();
      const lista = Array.isArray(resultado)
        ? resultado
        : resultado?.solicitacoes || [];

      if (lista.length === 0) {
        setSolicitacoes([]);
        setEstadoPainel(ESTADOS_PAINEL.VAZIO);
      } else {
        setSolicitacoes(lista);
        setEstadoPainel(ESTADOS_PAINEL.SUCESSO);
      }
    } catch (erro) {
      setMensagemErro(
        erro.message || "Erro ao carregar as solicitacoes pendentes."
      );
      setEstadoPainel(ESTADOS_PAINEL.ERRO);
    }
  }, []);

  useEffect(() => {
    carregarSolicitacoes();
  }, [carregarSolicitacoes]);

  const handleAvaliar = async (solicitacaoId, decisaoStatus) => {
    setProcessandoId(solicitacaoId);
    setErroAcao("");

    try {
      await avaliarSolicitacao(solicitacaoId, decisaoStatus);

      // Atualização imediata da lista local após confirmação de sucesso do backend.
      const novaLista = solicitacoes.filter((item) => item.id !== solicitacaoId);
      setSolicitacoes(novaLista);

      if (novaLista.length === 0) {
        setEstadoPainel(ESTADOS_PAINEL.VAZIO);
      }
    } catch (erro) {
      // Trata conflitos de concorrência (ex: 409 Conflict se outro protetor já avaliou) 
      // exibindo a mensagem do backend e sincronizando a lista novamente.
      setErroAcao(
        erro.message || "Nao foi possivel registrar a decisao para esta solicitacao."
      );
      await carregarSolicitacoes();
    } finally {
      setProcessandoId(null);
    }
  };

  const renderizarConteudo = () => {
    switch (estadoPainel) {
      case ESTADOS_PAINEL.CARREGANDO:
        return (
          <div className="flex justify-center items-center py-20" aria-live="polite">
            <span className="w-10 h-10 border-4 border-primaria border-t-transparent rounded-full animate-spin" />
            <span className="sr-only">Carregando solicitacoes...</span>
          </div>
        );

      case ESTADOS_PAINEL.ERRO:
        return (
          <div className="text-center py-16 px-4 bg-white rounded-xl border border-borda">
            <h2 className="text-xl font-bold text-erro mb-2">
              Falha ao carregar o painel
            </h2>
            <p className="text-textoCorpo mb-6">{mensagemErro}</p>
            <div className="max-w-xs mx-auto">
              <Button
                onClick={carregarSolicitacoes}
                variante="secundaria"
                fullWidth
              >
                Tentar novamente
              </Button>
            </div>
          </div>
        );

      case ESTADOS_PAINEL.VAZIO:
        return (
          <div className="text-center py-16 px-4 bg-white rounded-xl border border-borda">
            <h2 className="text-xl font-bold text-textoDestaque mb-2">
              Nenhuma solicitacao pendente
            </h2>
            <p className="text-textoApoio">
              Todas as solicitacoes de adocao ja foram avaliadas no momento.
            </p>
          </div>
        );

      case ESTADOS_PAINEL.SUCESSO:
        return (
          <div className="space-y-6">
            {solicitacoes.map((solicitacao) => {
              const estaProcessandoEsteCard = processandoId === solicitacao.id;
              const respostas = solicitacao.respostas || {};
              const nomeAnimal =
                solicitacao.animal_nome || solicitacao.animal?.nome || "Animal";
              const nomeAdotante =
                solicitacao.adotante_nome || solicitacao.adotante?.nome || "Adotante";

              return (
                <article
                  key={solicitacao.id}
                  className="bg-white rounded-xl border border-borda p-6 shadow-sm"
                >
                  {/* Hierarquia Visual: cabeçalho do card destaca o par Animal/Adotante e o badge semântico de status */}
                  <div className="flex flex-wrap items-center justify-between gap-4 pb-4 mb-4 border-b border-borda">
                    <div>
                      <span className="text-xs font-bold uppercase tracking-wider text-textoApoio">
                        Interesse em adotar
                      </span>
                      <h2 className="text-xl font-black text-textoDestaque">
                        {nomeAnimal}
                      </h2>
                      <p className="text-sm text-textoCorpo mt-0.5">
                        Candidato(a): <strong className="font-semibold">{nomeAdotante}</strong>
                      </p>
                    </div>

                    <span className="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide bg-alerta/20 text-textoDestaque border border-alerta">
                      {solicitacao.status || "PENDENTE"}
                    </span>
                  </div>

                  {/* Lei da Proximidade: respostas do questionário agrupadas em blocos internos de leitura */}
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                    <div className="bg-fundo p-3.5 rounded-lg border border-borda">
                      <h3 className="text-xs font-bold uppercase text-textoApoio mb-1">
                        Tipo de Moradia
                      </h3>
                      <p className="text-sm text-textoDestaque">
                        {respostas.tipoMoradia || "Nao informado"}
                      </p>
                    </div>

                    <div className="bg-fundo p-3.5 rounded-lg border border-borda">
                      <h3 className="text-xs font-bold uppercase text-textoApoio mb-1">
                        Rotina Diaria
                      </h3>
                      <p className="text-sm text-textoDestaque">
                        {respostas.rotinaDiaria || "Nao informado"}
                      </p>
                    </div>

                    <div className="bg-fundo p-3.5 rounded-lg border border-borda">
                      <h3 className="text-xs font-bold uppercase text-textoApoio mb-1">
                        Historico com Pets
                      </h3>
                      <p className="text-sm text-textoDestaque">
                        {respostas.historicoPets || "Nao informado"}
                      </p>
                    </div>
                  </div>

                  {/* Affordance e Máquina de Estados: ações desabilitadas durante a mutação para evitar requisições concorrentes */}
                  <div className="flex flex-wrap items-center justify-end gap-3">
                    <Button
                      type="button"
                      variante="secundaria"
                      disabled={estaProcessandoEsteCard}
                      onClick={() => handleAvaliar(solicitacao.id, "RECUSADA")}
                    >
                      Recusar
                    </Button>
                    <Button
                      type="button"
                      variante="primaria"
                      disabled={estaProcessandoEsteCard}
                      isLoading={estaProcessandoEsteCard}
                      onClick={() => handleAvaliar(solicitacao.id, "APROVADA")}
                    >
                      {estaProcessandoEsteCard ? "Processando..." : "Aprovar Adocao"}
                    </Button>
                  </div>
                </article>
              );
            })}
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <main className="min-h-screen bg-fundo px-4 py-8 md:py-12">
      <div className="max-w-5xl mx-auto">
        <header className="mb-8">
          <h1 className="text-3xl font-black text-textoDestaque tracking-tight">
            Painel do Protetor
          </h1>
          <p className="text-textoCorpo mt-2">
            Avalie as solicitacoes de adocao pendentes e os questionarios de triagem.
          </p>
        </header>

        {erroAcao && (
          <div
            role="alert"
            className="mb-6 p-4 rounded-lg bg-erro/10 border border-erro text-erro text-sm font-medium"
          >
            {erroAcao}
          </div>
        )}

        <section aria-label="Solicitacoes pendentes">
          {renderizarConteudo()}
        </section>
      </div>
    </main>
  );
};