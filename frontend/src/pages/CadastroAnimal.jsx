import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { cadastrarAnimal } from "../services/animalService";
import { Button } from "../components/Button";

const ESTADOS_ENVIO = {
  OCIOSO: "OCIOSO",
  CARREGANDO: "CARREGANDO",
  SUCESSO: "SUCESSO",
  ERRO: "ERRO",
};

export const CadastroAnimal = () => {
  const navigate = useNavigate();

  const [nome, setNome] = useState("");
  const [porte, setPorte] = useState("");
  const [tags, setTags] = useState("");
  const [arquivoFoto, setArquivoFoto] = useState(null);

  const [estadoEnvio, setEstadoEnvio] = useState(ESTADOS_ENVIO.OCIOSO);
  const [mensagemErro, setMensagemErro] = useState("");

  const estaCarregando = estadoEnvio === ESTADOS_ENVIO.CARREGANDO;

  const handleSubmit = async (evento) => {
    evento.preventDefault();

    if (!nome.trim() || !porte) {
      setMensagemErro("Preencha o nome e selecione o porte do animal.");
      setEstadoEnvio(ESTADOS_ENVIO.ERRO);
      return;
    }

    if (!arquivoFoto) {
      setMensagemErro("Selecione uma foto do animal para realizar o registro.");
      setEstadoEnvio(ESTADOS_ENVIO.ERRO);
      return;
    }

    setEstadoEnvio(ESTADOS_ENVIO.CARREGANDO);
    setMensagemErro("");

    try {
      await cadastrarAnimal(
        {
          nome: nome.trim(),
          porte,
          tags: tags.trim(),
        },
        arquivoFoto
      );

      setEstadoEnvio(ESTADOS_ENVIO.SUCESSO);
      setNome("");
      setPorte("");
      setTags("");
      setArquivoFoto(null);
    } catch (erro) {
      setMensagemErro(erro.message || "Falha ao registrar o animal.");
      setEstadoEnvio(ESTADOS_ENVIO.ERRO);
    }
  };

  return (
    <main className="min-h-screen bg-fundo px-4 py-8 md:py-12">
      <div className="max-w-xl mx-auto bg-white p-6 md:p-8 rounded-xl border border-borda">
        <header className="mb-8 border-b border-borda pb-4">
          <h1 className="text-2xl font-black text-textoDestaque tracking-tight">
            Registrar Resgate
          </h1>
          <p className="text-textoCorpo mt-1 text-sm">
            Insira os dados do animal para disponibiliza-lo para adocao.
          </p>
        </header>

        {estadoEnvio === ESTADOS_ENVIO.ERRO && (
          <div
            role="alert"
            className="mb-6 p-4 rounded-lg bg-erro/10 border border-erro text-erro text-sm font-medium"
          >
            {mensagemErro}
          </div>
        )}

        {estadoEnvio === ESTADOS_ENVIO.SUCESSO && (
          <div
            role="status"
            className="mb-6 p-4 rounded-lg bg-sucesso/10 border border-sucesso text-textoDestaque text-sm flex items-center justify-between gap-4"
          >
            <span className="font-medium">Animal registrado com sucesso no catalogo.</span>
            <button
              type="button"
              onClick={() => navigate("/")}
              className="underline font-bold text-textoDestaque hover:text-primaria cursor-pointer"
            >
              Ver catalogo
            </button>
          </div>
        )}

        {/* Lei da Proximidade: space-y-6 separa grupos de campos distintos, enquanto mb-1.5 aproxima o label do seu input */}
        <form onSubmit={handleSubmit} className="space-y-6" noValidate>
          <div>
            <label
              htmlFor="campo-nome"
              className="block text-sm font-semibold text-textoDestaque mb-1.5"
            >
              Nome do Animal *
            </label>
            <input
              id="campo-nome"
              type="text"
              required
              disabled={estaCarregando}
              value={nome}
              onChange={(e) => setNome(e.target.value)}
              placeholder="Ex: Thor, Mel..."
              className="w-full px-3.5 py-2.5 bg-white border border-borda rounded-lg text-textoDestaque placeholder-textoApoio focus:outline-none focus:ring-2 focus:ring-primaria disabled:opacity-50 disabled:cursor-not-allowed"
            />
          </div>

          <div>
            <label
              htmlFor="campo-porte"
              className="block text-sm font-semibold text-textoDestaque mb-1.5"
            >
              Porte *
            </label>
            <select
              id="campo-porte"
              required
              disabled={estaCarregando}
              value={porte}
              onChange={(e) => setPorte(e.target.value)}
              className="w-full px-3.5 py-2.5 bg-white border border-borda rounded-lg text-textoDestaque focus:outline-none focus:ring-2 focus:ring-primaria disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
            >
              <option value="">Selecione o porte...</option>
              <option value="PEQUENO">Pequeno</option>
              <option value="MEDIO">Medio</option>
              <option value="GRANDE">Grande</option>
            </select>
          </div>

          <div>
            <label
              htmlFor="campo-tags"
              className="block text-sm font-semibold text-textoDestaque mb-1.5"
            >
              Caracteristicas (Tags)
            </label>
            <input
              id="campo-tags"
              type="text"
              disabled={estaCarregando}
              value={tags}
              onChange={(e) => setTags(e.target.value)}
              placeholder="Ex: Docil, Vacinado, Castrado"
              className="w-full px-3.5 py-2.5 bg-white border border-borda rounded-lg text-textoDestaque placeholder-textoApoio focus:outline-none focus:ring-2 focus:ring-primaria disabled:opacity-50 disabled:cursor-not-allowed"
            />
            <span className="block text-xs text-textoApoio mt-1">
              Separe cada caracteristica por virgula.
            </span>
          </div>

          <div>
            <label
              htmlFor="campo-foto"
              className="block text-sm font-semibold text-textoDestaque mb-1.5"
            >
              Foto do Animal *
            </label>
            <input
              id="campo-foto"
              type="file"
              accept="image/jpeg,image/png,image/webp"
              required
              disabled={estaCarregando}
              onChange={(e) => setArquivoFoto(e.target.files?.[0] || null)}
              className="w-full text-sm text-textoCorpo file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-secundaria/20 file:text-textoDestaque hover:file:bg-secundaria/30 file:cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
            />
          </div>

          {/* Máquina de Estados: botão desabilitado durante o envio para impedir duplicidade de registros no banco */}
          <div className="pt-2">
            <Button
              type="submit"
              variante="primaria"
              fullWidth
              disabled={estaCarregando}
              isLoading={estaCarregando}
            >
              {estaCarregando ? "Salvando Registro..." : "Salvar Registro"}
            </Button>
          </div>
        </form>
      </div>
    </main>
  );
};