// Centraliza a representação visual da máquina de estados descrita no blueprint.
// Nenhuma cor ou string mágica deve vazar para os componentes de UI.

export const ANIMAL_STATUS_UI = {
  DISPONIVEL: {
    label: 'Disponível',
    corFundo: 'bg-primaria/20',
    corTexto: 'text-textoDestaque'
  },
  EM_PROCESSO: {
    label: 'Em Processo',
    corFundo: 'bg-alerta/20',
    corTexto: 'text-alerta'
  },
  ADOTADO: {
    label: 'Adotado',
    corFundo: 'bg-secundaria/20',
    corTexto: 'text-secundaria'
  }
};

export const SOLICITACAO_STATUS_UI = {
  PENDENTE: {
    label: 'Aguardando Análise',
    corFundo: 'bg-borda/30',
    corTexto: 'text-textoApoio'
  },
  EM_ANALISE: {
    label: 'Em Análise',
    corFundo: 'bg-alerta/20',
    corTexto: 'text-alerta'
  },
  APROVADA: {
    label: 'Aprovada',
    corFundo: 'bg-sucesso/20',
    corTexto: 'text-sucesso'
  },
  RECUSADA: {
    label: 'Recusada',
    corFundo: 'bg-erro/20',
    corTexto: 'text-erro'
  }
};