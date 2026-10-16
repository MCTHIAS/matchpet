import uuid
from typing import Dict
from domain.entities import (
    Usuario,
    QuestionarioTriagem,
    SolicitacaoAdocao,
    StatusSolicitacao
)
from domain.exceptions import RegraNegocioException
from use_cases.interfaces.solicitacao_repository_interface import SolicitacaoRepositoryInterface
from use_cases.interfaces.animal_repository_interface import AnimalRepositoryInterface

PAPEL_USUARIO_ADOTANTE = "ADOTANTE"


class EnviarSolicitacaoAdocao:
    def __init__(
        self,
        repositorio_solicitacao: SolicitacaoRepositoryInterface,
        repositorio_animal: AnimalRepositoryInterface
    ):
        self.repositorio_solicitacao = repositorio_solicitacao
        self.repositorio_animal = repositorio_animal

    def executar(
        self,
        animal_id: uuid.UUID,
        adotante_id: uuid.UUID,
        nome_adotante: str,
        email_adotante: str,
        respostas_questionario: Dict[str, str]
    ) -> uuid.UUID:
        animal = self.repositorio_animal.buscar_por_id(animal_id)

        if not animal.esta_disponivel():
            raise RegraNegocioException("Este animal nao esta disponivel para receber solicitacoes.")

        usuario_adotante = Usuario(
            id=adotante_id,
            nome=nome_adotante,
            papel=PAPEL_USUARIO_ADOTANTE,
            email=email_adotante
        )

        # Regra: questionario de triagem e obrigatorio para registrar uma solicitacao de adocao.
        questionario = QuestionarioTriagem(
            id=uuid.uuid4(),
            adotante_id=usuario_adotante.id,
            respostas=respostas_questionario
        )
        questionario.avaliar_compatibilidade()

        nova_solicitacao = SolicitacaoAdocao(
            id=uuid.uuid4(),
            animal_id=animal.id,
            adotante_id=usuario_adotante.id,
            status=StatusSolicitacao.PENDENTE
        )

        self.repositorio_solicitacao.salvar_solicitacao_com_triagem(
            usuario_adotante=usuario_adotante,
            questionario=questionario,
            solicitacao=nova_solicitacao
        )
        return nova_solicitacao.id