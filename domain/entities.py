import uuid
from enum import Enum
from typing import List, Dict, Optional
from domain.exceptions import TransicaoStatusInvalidaException, RegraNegocioException

QUANTIDADE_MINIMA_RESPOSTAS_TRIAGEM = 1


class StatusAnimal(Enum):
    DISPONIVEL = "DISPONIVEL"
    EM_PROCESSO = "EM_PROCESSO"
    ADOTADO = "ADOTADO"


class StatusSolicitacao(Enum):
    PENDENTE = "PENDENTE"
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
        if not self.nome or not self.nome.strip():
            raise RegraNegocioException("O nome do usuario e obrigatorio.")
        if not self.email or "@" not in self.email:
            raise RegraNegocioException("O e-mail do usuario e invalido.")
        if not self.papel or not self.papel.strip():
            raise RegraNegocioException("O papel do usuario e obrigatorio.")


class Animal:
    def __init__(
        self,
        id: uuid.UUID,
        protetor_id: uuid.UUID,
        nome: str,
        porte: str,
        tags: List[str],
        status: StatusAnimal,
        foto_url: Optional[str] = None
    ):
        if not nome or not nome.strip():
            raise RegraNegocioException("O nome do animal e obrigatorio.")
        if not porte or not porte.strip():
            raise RegraNegocioException("O porte do animal e obrigatorio.")

        self.id = id
        self.protetor_id = protetor_id
        self.nome = nome.strip()
        self.porte = porte.strip()
        self.tags = tags
        self.status = status
        self.foto_url = foto_url

    def marcar_em_processo(self) -> None:
        # Regra: ciclo de vida do animal exige que ele esteja DISPONIVEL antes de entrar EM_PROCESSO.
        if self.status != StatusAnimal.DISPONIVEL:
            raise TransicaoStatusInvalidaException(
                "Apenas animais disponiveis podem entrar em processo de adocao."
            )
        self.status = StatusAnimal.EM_PROCESSO

    def marcar_adotado(self) -> None:
        # Regra: animais adotados saem do catalogo publico apos aceite final do protetor.
        if self.status not in (StatusAnimal.DISPONIVEL, StatusAnimal.EM_PROCESSO):
            raise TransicaoStatusInvalidaException(
                "O animal nao esta em um estado valido para ser marcado como adotado."
            )
        self.status = StatusAnimal.ADOTADO

    def esta_disponivel(self) -> bool:
        return self.status == StatusAnimal.DISPONIVEL


class QuestionarioTriagem:
    def __init__(self, id: uuid.UUID, adotante_id: uuid.UUID, respostas: Dict[str, str]):
        self.id = id
        self.adotante_id = adotante_id
        self.respostas = respostas

    def avaliar_compatibilidade(self) -> bool:
        # Regra: a triagem e obrigatoria; respostas vazias ou incompletas invalidam a compatibilidade.
        if not self.respostas or len(self.respostas) < QUANTIDADE_MINIMA_RESPOSTAS_TRIAGEM:
            raise RegraNegocioException("O preenchimento do questionario de triagem e obrigatorio.")

        for chave_pergunta, texto_resposta in self.respostas.items():
            if not str(texto_resposta).strip():
                raise RegraNegocioException(
                    f"A resposta para o campo '{chave_pergunta}' do questionario nao pode estar vazia."
                )
        return True


class SolicitacaoAdocao:
    def __init__(
        self,
        id: uuid.UUID,
        animal_id: uuid.UUID,
        adotante_id: uuid.UUID,
        status: StatusSolicitacao
    ):
        self.id = id
        self.animal_id = animal_id
        self.adotante_id = adotante_id
        self.status = status

    def iniciar_analise(self) -> None:
        # Regra: transiciona de PENDENTE para EM_ANALISE quando o protetor abre/avalia a ficha.
        if self.status != StatusSolicitacao.PENDENTE:
            raise TransicaoStatusInvalidaException(
                "Apenas solicitacoes pendentes podem iniciar analise."
            )
        self.status = StatusSolicitacao.EM_ANALISE

    def aprovar(self) -> None:
        # Regra: a aprovacao ocorre sobre uma solicitacao que esta EM_ANALISE.
        if self.status != StatusSolicitacao.EM_ANALISE:
            raise TransicaoStatusInvalidaException(
                "Apenas solicitacoes em analise podem ser aprovadas."
            )
        self.status = StatusSolicitacao.APROVADA

    def recusar(self) -> None:
        # Regra: uma solicitacao pode ser recusada durante a analise ou automaticamente quando outra e aprovada.
        if self.status not in (StatusSolicitacao.PENDENTE, StatusSolicitacao.EM_ANALISE):
            raise TransicaoStatusInvalidaException(
                "A solicitacao nao esta em um estado valido para recusa."
            )
        self.status = StatusSolicitacao.RECUSADA