import uuid
from domain.entities import StatusSolicitacao
from use_cases.interfaces.solicitacao_repository_interface import SolicitacaoRepositoryInterface
from use_cases.interfaces.animal_repository_interface import AnimalRepositoryInterface

class AvaliarSolicitacao:
    def __init__(self, solicitacao_repository: SolicitacaoRepositoryInterface, animal_repository: AnimalRepositoryInterface):
        self.solicitacao_repository = solicitacao_repository
        self.animal_repository = animal_repository

    def executar(self, solicitacao_id: uuid.UUID, aprovar: bool) -> None:
        solicitacao = self.solicitacao_repository.buscar_por_id(solicitacao_id)
        
        # Armazena o status original para controle de concorrência no adaptador
        status_anterior = solicitacao.status
        
        if aprovar:
            solicitacao.aprovar()
        else:
            solicitacao.recusar()

        # Tenta persistir a mudança de status passando a responsabilidade do lock pro repository
        self.solicitacao_repository.salvar_avaliacao(solicitacao, status_anterior)

        # Regra: Quando aprovada, o animal muda de status e concorrência é encerrada[cite: 1]
        if aprovar:
            animal = self.animal_repository.buscar_por_id(solicitacao.animal_id)
            animal.marcar_adotado()
            self.animal_repository.salvar(animal)
            
            motivo_recusa = "O animal já foi adotado por outra pessoa."
            self.solicitacao_repository.recusar_outras_solicitacoes(
                animal_id=solicitacao.animal_id, 
                solicitacao_aprovada_id=solicitacao.id, 
                motivo=motivo_recusa
            )