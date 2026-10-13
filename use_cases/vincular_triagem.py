import uuid
from use_cases.interfaces.solicitacao_repository_interface import SolicitacaoRepositoryInterface

class VincularTriagem:
    """
    Caso de uso nascido da hipótese de mitigar fricção de onboarding.
    Ocorre após a submissão do formulário, avançando o fluxo da solicitação.
    """
    def __init__(self, solicitacao_repository: SolicitacaoRepositoryInterface):
        self.solicitacao_repository = solicitacao_repository

    def executar(self, solicitacao_id: uuid.UUID, questionario_id: uuid.UUID) -> None:
        solicitacao = self.solicitacao_repository.buscar_por_id(solicitacao_id)
        
        # A regra de negócio dentro da entidade garante que o status inicial era correto
        solicitacao.vincular_questionario(questionario_id)
        
        self.solicitacao_repository.salvar(solicitacao)