import uuid
from enum import Enum
from typing import List, Dict, Optional
from domain.exceptions import TransicaoStatusInvalidaException, RegraNegocioException

class StatusAnimal(Enum):
    DISPONIVEL = "DISPONIVEL"
    EM_PROCESSO = "EM_PROCESSO"
    ADOTADO = "ADOTADO"

class StatusSolicitacao(Enum):
    AGUARDANDO_TRIAGEM = "AGUARDANDO_TRIAGEM"
    EM_ANALISE = "EM_ANALISE"
    APROVADA = "APROVADA"
    RECUSADA = "RECUSADA"

class Usuario:
    def __init__(self, id: uuid.UUID, nome: str, papel: str, email: str):
        self.id = id
        self.nome = nome
        self.papel = papel
        self.email = email
        self.validar_cadastro()

    def validar_cadastro(self) -> None:
        if not self.nome or not self.email:
            raise RegraNegocioException("Usuário deve conter nome e e-mail válidos.")

class Animal:
    def __init__(self, id: uuid.UUID, protetor_id: uuid.UUID, nome: str, porte: str, tags: List[str], status: StatusAnimal):
        self.id = id
        self.protetor_id = protetor_id
        self.nome = nome
        self.porte = porte
        self.tags = tags
        self.status = status

    def marcar_em_processo(self) -> None:
        if self.status != StatusAnimal.DISPONIVEL:
            raise TransicaoStatusInvalidaException("Apenas animais disponíveis podem entrar em processo de adoção.")
        self.status = StatusAnimal.EM_PROCESSO

    def marcar_adotado(self) -> None:
        # Regra: animais adotados saem do catálogo público[cite: 1]
        if self.status not in [StatusAnimal.DISPONIVEL, StatusAnimal.EM_PROCESSO]:
            raise TransicaoStatusInvalidaException("O animal não está em um estado válido para ser adotado.")
        self.status = StatusAnimal.ADOTADO

    def esta_disponivel(self) -> bool:
        return self.status == StatusAnimal.DISPONIVEL

class QuestionarioTriagem:
    def __init__(self, id: uuid.UUID, adotante_id: uuid.UUID, respostas: Dict[str, str]):
        self.id = id
        self.adotante_id = adotante_id
        self.respostas = respostas

    def avaliar_compatibilidade(self) -> int:
        # A lógica real de escoragem entraria aqui. 
        # Retorna um score de compatibilidade baseado nas respostas.
        return 100

class SolicitacaoAdocao:
    def __init__(self, id: uuid.UUID, animal_id: uuid.UUID, adotante_id: uuid.UUID, status: StatusSolicitacao, questionario_id: Optional[uuid.UUID] = None):
        self.id = id
        self.animal_id = animal_id
        self.adotante_id = adotante_id
        self.status = status
        self.questionario_id = questionario_id

    def vincular_questionario(self, questionario_id: uuid.UUID) -> None:
        # Regra: Transição para mitigar fricção inicial. Só avança para análise com questionário vinculado.
        if self.status != StatusSolicitacao.AGUARDANDO_TRIAGEM:
            raise TransicaoStatusInvalidaException("Questionário só pode ser vinculado em solicitações aguardando triagem.")
        self.questionario_id = questionario_id
        self.status = StatusSolicitacao.EM_ANALISE

    def iniciar_analise(self) -> None:
        if self.status != StatusSolicitacao.EM_ANALISE:
            raise TransicaoStatusInvalidaException("A solicitação precisa ter um questionário vinculado para iniciar análise.")

    def aprovar(self) -> None:
        if self.status != StatusSolicitacao.EM_ANALISE:
            raise TransicaoStatusInvalidaException("Apenas solicitações em análise podem ser aprovadas.")
        self.status = StatusSolicitacao.APROVADA

    def recusar(self) -> None:
        if self.status not in [StatusSolicitacao.AGUARDANDO_TRIAGEM, StatusSolicitacao.EM_ANALISE]:
            raise TransicaoStatusInvalidaException("A solicitação não está em um estado válido para recusa.")
        self.status = StatusSolicitacao.RECUSADA