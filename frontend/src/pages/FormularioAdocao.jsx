import React, { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { enviarSolicitacaoAdocao } from "../services/adocaoService";
import { Button } from "../components/Button";

const ESTADOS_SUBMISSAO = {
  OCIOSO: "OCIOSO",
  CARREGANDO: "CARREGANDO",
  SUCESSO: "SUCESSO",
  ERRO: "ERRO",
};

export const FormularioAdocao = () => {
  const { animalId } = useParams();
  const navigate = useNavigate();

  const [nome, setNome] = useState("");
  const [email, setEmail] = useState("");
  const [tipoMoradia, setTipoMoradia] = useState("");
  const [rotinaDiaria, setRotinaDiaria] = useState("");
  const [historicoPets, setHistoricoPets] = useState("");

  const [estadoSubmissao, setEstadoSubmissao] = useState(ESTADOS_SUBMISSAO.OCIOSO);
  const [mensagemErro, setMensagemErro] = useState("");

  const estaEnviando = estadoSubmissao === ESTADOS_SUBMISSAO.CARREGANDO;

  const handleSubmit = async (evento) => {
    evento.preventDefault();

    // Pré-validação sincronizada com as invariantes das entidades Usuario e QuestionarioTriagem.
    if (
      !nome.trim() ||
      !email.trim() ||
      !tipoMoradia.trim() ||
      !rotinaDiaria.trim() ||
      !historicoPets.trim()
    ) {
      setMensagemErro(
        "Todos os campos de identificacao e perguntas do questionario sao obrigatorios."
      );
      setEstadoSubmissao(ESTADOS_SUBMISSAO.ERRO);
      return;
    }

    setEstadoSubmissao(ESTADOS_SUBMISSAO.CARREGANDO);
    setMensagemErro("");

    try {
      await enviarSolicitacaoAdocao({
        animal_id: animalId,
        nome: nome.trim(),
        email: email.trim(),
        respostas: {
          tipoMoradia: tipoMoradia.trim(),
          rotinaDiaria: rotinaDiaria.trim(),
          historicoPets: historicoPets.trim(),
        },
      });

      setEstadoSubmissao(ESTADOS_SUBMISSAO.SUCESSO);
    } catch (erro) {
      setMensagemErro(erro.message || "Nao foi possivel enviar sua solicitacao de adocao.");
      setEstadoSubmissao(ESTADOS_SUBMISSAO.ERRO);
    }
  };

  if (estadoSubmissao === ESTADOS_SUBMISSAO.SUCESSO) {
    return (
      <main className="min-h-screen bg-fundo px-4 py-12">
        <div className="max-w-lg mx-auto bg-white p-8 rounded-xl border border-borda text-center">
          <h1 className="text-2xl font-black text-textoDestaque mb-3">
            Solicitacao Enviada com Sucesso
          </h1>
          <p className="text-textoCorpo mb-6">
            Suas respostas de triagem foram vinculadas ao animal e encaminhadas para avaliacao do protetor responsavel.
          </p>
          <Button variante="primaria" fullWidth onClick={() => navigate("/")}>
            Voltar para o Catalogo
          </Button>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-fundo px-4 py-8 md:py-12">
      <div className="max-w-2xl mx-auto bg-white p-6 md:p-8 rounded-xl border border-borda">
        <header className="mb-8 border-b border-borda pb-4">
          <h1 className="text-2xl font-black text-textoDestaque tracking-tight">
            Questionario de Triagem para Adocao
          </h1>
          <p className="text-textoCorpo mt-1 text-sm">
            Preencha seus dados e responda as perguntas obrigatorias para iniciar o processo de adocao responsavel.
          </p>
        </header>

        {estadoSubmissao === ESTADOS_SUBMISSAO.ERRO && (
          <div
            role="alert"
            className="mb-6 p-4 rounded-lg bg-erro/10 border border-erro text-erro text-sm font-medium"
          >
            {mensagemErro}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-8" noValidate>
          {/* Lei da Proximidade: agrupa os dados de identificação do adotante em uma seção distinta das respostas de triagem */}
          <fieldset className="space-y-4">
            <legend className="text-lg font-bold text-textoDestaque mb-2">
              1. Seus Dados de Contato
            </legend>

            <div>
              <label
                htmlFor="adotante-nome"
                className="block text-sm font-semibold text-textoDestaque mb-1.5"
              >
                Nome Completo *
              </label>
              <input
                id="adotante-nome"
                type="text"
                required
                disabled={estaEnviando}
                value={nome}
                onChange={(e) => setNome(e.target.value)}
                placeholder="Digite seu nome completo"
                className="w-full px-3.5 py-2.5 bg-white border border-borda rounded-lg text-textoDestaque placeholder-textoApoio focus:outline-none focus:ring-2 focus:ring-primaria disabled:opacity-50"
              />
            </div>

            <div>
              <label
                htmlFor="adotante-email"
                className="block text-sm font-semibold text-textoDestaque mb-1.5"
              >
                E-mail para Contato *
              </label>
              <input
                id="adotante-email"
                type="email"
                required
                disabled={estaEnviando}
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="seuemail@exemplo.com"
                className="w-full px-3.5 py-2.5 bg-white border border-borda rounded-lg text-textoDestaque placeholder-textoApoio focus:outline-none focus:ring-2 focus:ring-primaria disabled:opacity-50"
              />
            </div>
          </fieldset>

          <hr className="border-borda" />

          <fieldset className="space-y-4">
            <legend className="text-lg font-bold text-textoDestaque mb-2">
              2. Ambiente e Rotina
            </legend>

            <div>
              <label
                htmlFor="triagem-moradia"
                className="block text-sm font-semibold text-textoDestaque mb-1.5"
              >
                Tipo de Moradia e Seguranca *
              </label>
              <textarea
                id="triagem-moradia"
                rows={3}
                required
                disabled={estaEnviando}
                value={tipoMoradia}
                onChange={(e) => setTipoMoradia(e.target.value)}
                placeholder="Descreva se mora em casa ou apartamento, se ha quintal murado ou janelas teladas."
                className="w-full px-3.5 py-2.5 bg-white border border-borda rounded-lg text-textoDestaque placeholder-textoApoio focus:outline-none focus:ring-2 focus:ring-primaria disabled:opacity-50"
              />
            </div>

            <div>
              <label
                htmlFor="triagem-rotina"
                className="block text-sm font-semibold text-textoDestaque mb-1.5"
              >
                Rotina Diaria *
              </label>
              <textarea
                id="triagem-rotina"
                rows={3}
                required
                disabled={estaEnviando}
                value={rotinaDiaria}
                onChange={(e) => setRotinaDiaria(e.target.value)}
                placeholder="Quantas horas o animal ficara sozinho por dia e quem cuidara dos passeios?"
                className="w-full px-3.5 py-2.5 bg-white border border-borda rounded-lg text-textoDestaque placeholder-textoApoio focus:outline-none focus:ring-2 focus:ring-primaria disabled:opacity-50"
              />
            </div>

            <div>
              <label
                htmlFor="triagem-historico"
                className="block text-sm font-semibold text-textoDestaque mb-1.5"
              >
                Historico com Outros Animais *
              </label>
              <textarea
                id="triagem-historico"
                rows={3}
                required
                disabled={estaEnviando}
                value={historicoPets}
                onChange={(e) => setHistoricoPets(e.target.value)}
                placeholder="Voce ja teve ou tem outros pets em casa? Como e a convivencia?"
                className="w-full px-3.5 py-2.5 bg-white border border-borda rounded-lg text-textoDestaque placeholder-textoApoio focus:outline-none focus:ring-2 focus:ring-primaria disabled:opacity-50"
              />
            </div>
          </fieldset>

          {/* Hierarquia Visual: ação primária em destaque à direita e ação secundária neutra à esquerda */}
          <div className="flex flex-col-reverse sm:flex-row items-center justify-end gap-3 pt-4 border-t border-borda">
            <Button
              type="button"
              variante="secundaria"
              disabled={estaEnviando}
              onClick={() => navigate("/")}
            >
              Cancelar
            </Button>
            <Button
              type="submit"
              variante="primaria"
              disabled={estaEnviando}
              isLoading={estaEnviando}
            >
              {estaEnviando ? "Enviando Solicitacao..." : "Enviar Solicitacao de Adocao"}
            </Button>
          </div>
        </form>
      </div>
    </main>
  );
};