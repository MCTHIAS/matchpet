from abc import ABC, abstractmethod
import uuid
from domain.entities import SolicitacaoAdocao, StatusSolicitacao

class SolicitacaoRepositoryInterface(ABC):
    
    @abstractmethod
    def salvar(self, solicitacao: SolicitacaoAdocao) -> None:
        pass
        
    @abstractmethod
    def salvar_avaliacao(self, solicitacao: SolicitacaoAdocao, status_anterior: StatusSolicitacao) -> None:
        """
        Implementa o controle de concorrência otimista. 
        Deve lançar ConcorrenciaSolicitacaoException se a linha no banco já sofreu mutação.
        """
        pass

    @abstractmethod
    def buscar_por_id(self, id: uuid.UUID) -> SolicitacaoAdocao:
        pass

    @abstractmethod
    def recusar_outras_solicitacoes(self, animal_id: uuid.UUID, solicitacao_aprovada_id: uuid.UUID, motivo: str) -> None:
        """
        Garante a transição de estado em lote para outras solicitações concorrentes[cite: 1].
        """
        pass