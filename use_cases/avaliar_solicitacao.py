import uuid
from typing import List
from domain.entities import StatusSolicitacao
from use_cases.interfaces.solicitacao_repository_interface import (
    SolicitacaoRepositoryInterface,
    SolicitacaoParaAvaliacaoDTO
)
from use_cases.interfaces.animal_repository_interface import AnimalRepositoryInterface

MOTIVO_RECUSA_AUTOMATICA_ADOCAO = "O animal ja foi adotado em outra solicitacao aprovada."


class AvaliarSolicitacao:
    def __init__(
        self,
        repositorio_solicitacao: SolicitacaoRepositoryInterface,
        repositorio_animal: AnimalRepositoryInterface
    ):
        self.repositorio_solicitacao = repositorio_solicitacao
        self.repositorio_animal = repositorio_animal

    def listar_pendentes(self) -> List[SolicitacaoParaAvaliacaoDTO]:
        return self.repositorio_solicitacao.listar_por_status(StatusSolicitacao.PENDENTE)

    def executar(self, solicitacao_id: uuid.UUID, aprovar: bool) -> None:
        solicitacao = self.repositorio_solicitacao.buscar_por_id(solicitacao_id)
        animal = self.repositorio_animal.buscar_por_id(solicitacao.animal_id)
        status_original_no_banco = solicitacao.status

        # Regra: se a solicitacao estava PENDENTE, o ato de avaliar inicia a analise do protetor
        # e coloca o animal EM_PROCESSO antes da decisao final.
        if solicitacao.status == StatusSolicitacao.PENDENTE:
            solicitacao.iniciar_analise()
            if animal.esta_disponivel():
                animal.marcar_em_processo()

        if aprovar:
            solicitacao.aprovar()
        else:
            solicitacao.recusar()

        self.repositorio_solicitacao.salvar_avaliacao(
            solicitacao=solicitacao,
            status_anterior=status_original_no_banco
        )

        # Nota Arquitetural obrigatoria do Blueprint: quando uma solicitacao e APROVADA,
        # o animal passa para ADOTADO e todas as outras solicitacoes PENDENTES ou EM_ANALISE
        # do mesmo animal transicionam para RECUSADA automaticamente.
        if aprovar:
            animal.marcar_adotado()
            self.repositorio_animal.salvar(animal)
            self.repositorio_solicitacao.recusar_outras_solicitacoes_do_animal(
                animal_id=solicitacao.animal_id,
                solicitacao_aprovada_id=solicitacao.id,
                motivo_recusa=MOTIVO_RECUSA_AUTOMATICA_ADOCAO
            )