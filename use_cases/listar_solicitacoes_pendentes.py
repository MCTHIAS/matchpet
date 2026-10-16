from typing import List
from domain.entities import StatusSolicitacao
from use_cases.interfaces.solicitacao_repository_interface import SolicitacaoRepositoryInterface
from use_cases.dtos import SolicitacaoPendenteDTO

class ListarSolicitacoesPendentes:
    def __init__(self, solicitacao_repository: SolicitacaoRepositoryInterface):
        self.solicitacao_repository = solicitacao_repository

    def executar(self) -> List[SolicitacaoPendenteDTO]:
        # Busca todas as solicitações que já passaram pelo onboarding do questionário
        return self.solicitacao_repository.listar_por_status(StatusSolicitacao.EM_ANALISE)