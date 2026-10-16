from abc import ABC, abstractmethod
from dataclasses import dataclass
import uuid
from typing import List, Dict
from domain.entities import SolicitacaoAdocao, StatusSolicitacao, QuestionarioTriagem, Usuario


@dataclass(frozen=True)
class SolicitacaoParaAvaliacaoDTO:
    """Dados consolidados da solicitacao, adotante, animal e triagem para o painel do protetor."""
    id: uuid.UUID
    animal_id: uuid.UUID
    animal_nome: str
    adotante_id: uuid.UUID
    adotante_nome: str
    status: str
    respostas_triagem: Dict[str, str]


class SolicitacaoRepositoryInterface(ABC):
    @abstractmethod
    def salvar_solicitacao_com_triagem(
        self,
        usuario_adotante: Usuario,
        questionario: QuestionarioTriagem,
        solicitacao: SolicitacaoAdocao
    ) -> None:
        pass

    @abstractmethod
    def salvar_avaliacao(
        self,
        solicitacao: SolicitacaoAdocao,
        status_anterior: StatusSolicitacao
    ) -> None:
        pass

    @abstractmethod
    def buscar_por_id(self, solicitacao_id: uuid.UUID) -> SolicitacaoAdocao:
        pass

    @abstractmethod
    def recusar_outras_solicitacoes_do_animal(
        self,
        animal_id: uuid.UUID,
        solicitacao_aprovada_id: uuid.UUID,
        motivo_recusa: str
    ) -> None:
        pass

    @abstractmethod
    def listar_por_status(self, status: StatusSolicitacao) -> List[SolicitacaoParaAvaliacaoDTO]:
        pass