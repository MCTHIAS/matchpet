import uuid
from domain.entities import SolicitacaoAdocao, StatusSolicitacao
from use_cases.interfaces.solicitacao_repository_interface import SolicitacaoRepositoryInterface
from use_cases.interfaces.animal_repository_interface import AnimalRepositoryInterface
from domain.exceptions import RegraNegocioException

class EnviarSolicitacaoAdocao:
    def __init__(self, solicitacao_repository: SolicitacaoRepositoryInterface, animal_repository: AnimalRepositoryInterface):
        self.solicitacao_repository = solicitacao_repository
        self.animal_repository = animal_repository

    def executar(self, animal_id: uuid.UUID, adotante_id: uuid.UUID) -> uuid.UUID:
        animal = self.animal_repository.buscar_por_id(animal_id)
        
        if not animal.esta_disponivel():
            raise RegraNegocioException("Animal não está disponível para adoção.")

        # Inicia a solicitação sem questionário para reduzir fricção no onboarding
        nova_solicitacao = SolicitacaoAdocao(
            id=uuid.uuid4(),
            animal_id=animal_id,
            adotante_id=adotante_id,
            status=StatusSolicitacao.AGUARDANDO_TRIAGEM
        )
        
        self.solicitacao_repository.salvar(nova_solicitacao)
        return nova_solicitacao.id