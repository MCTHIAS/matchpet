import { fetchApi } from "./api";

export async function enviarSolicitacaoAdocao(dadosSolicitacao) {
  // Contrato estruturado para permitir que o AdocaoController instancie simultaneamente 
  // o Usuario adotante, o QuestionarioTriagem e a SolicitacaoAdocao.
  const payload = {
    animal_id: dadosSolicitacao.animal_id,
    nome: dadosSolicitacao.nome,
    email: dadosSolicitacao.email,
    respostas: {
      tipoMoradia: dadosSolicitacao.respostas.tipoMoradia,
      rotinaDiaria: dadosSolicitacao.respostas.rotinaDiaria,
      historicoPets: dadosSolicitacao.respostas.historicoPets,
    },
  };

  return fetchApi("/solicitacoes", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function listarSolicitacoesPendentes() {
  return fetchApi("/solicitacoes?status=PENDENTE");
}

export async function avaliarSolicitacao(solicitacaoId, decisaoStatus) {
  // Restringe o payload ao contrato estrito da máquina de estados de domínio ('APROVADA' ou 'RECUSADA').
  return fetchApi(`/solicitacoes/${solicitacaoId}/avaliar`, {
    method: "POST",
    body: JSON.stringify({ status: decisaoStatus }),
  });
}