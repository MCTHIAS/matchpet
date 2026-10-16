import uuid
from typing import List, Dict
from supabase import Client
from domain.entities import (
    SolicitacaoAdocao,
    StatusSolicitacao,
    QuestionarioTriagem,
    Usuario
)
from domain.exceptions import ConcorrenciaSolicitacaoException, RegraNegocioException
from use_cases.interfaces.solicitacao_repository_interface import (
    SolicitacaoRepositoryInterface,
    SolicitacaoParaAvaliacaoDTO
)

NOME_TABELA_USUARIOS = "usuarios"
NOME_TABELA_QUESTIONARIOS = "questionarios_triagem"
NOME_TABELA_SOLICITACOES = "solicitacoes_adocao"


class SupabaseSolicitacaoRepository(SolicitacaoRepositoryInterface):
    def __init__(self, cliente_supabase: Client):
        self.cliente = cliente_supabase

    def salvar_solicitacao_com_triagem(
        self,
        usuario_adotante: Usuario,
        questionario: QuestionarioTriagem,
        solicitacao: SolicitacaoAdocao
    ) -> None:
        # Regra: persiste usuario, questionario_triagem e solicitacao_adocao respeitando
        # a ordem das chaves estrangeiras definidas no esquema PostgreSQL.
        dados_usuario = {
            "id": str(usuario_adotante.id),
            "nome": usuario_adotante.nome,
            "papel": usuario_adotante.papel,
            "email": usuario_adotante.email
        }
        self.cliente.table(NOME_TABELA_USUARIOS).upsert(dados_usuario).execute()

        dados_questionario = {
            "id": str(questionario.id),
            "adotante_id": str(questionario.adotante_id),
            "respostas": questionario.respostas
        }
        self.cliente.table(NOME_TABELA_QUESTIONARIOS).upsert(dados_questionario).execute()

        dados_solicitacao = {
            "id": str(solicitacao.id),
            "animal_id": str(solicitacao.animal_id),
            "adotante_id": str(solicitacao.adotante_id),
            "status": solicitacao.status.value
        }
        self.cliente.table(NOME_TABELA_SOLICITACOES).upsert(dados_solicitacao).execute()

    def salvar_avaliacao(
        self,
        solicitacao: SolicitacaoAdocao,
        status_anterior: StatusSolicitacao
    ) -> None:
        # Regra: controle de concorrencia otimista; atualiza apenas se o status no banco
        # ainda for identico ao status lido no inicio do caso de uso.
        resposta = (
            self.cliente.table(NOME_TABELA_SOLICITACOES)
            .update({"status": solicitacao.status.value})
            .eq("id", str(solicitacao.id))
            .eq("status", status_anterior.value)
            .execute()
        )

        if not resposta.data:
            raise ConcorrenciaSolicitacaoException(
                "Esta solicitacao ja foi avaliada simultaneamente por outro protetor."
            )

    def buscar_por_id(self, solicitacao_id: uuid.UUID) -> SolicitacaoAdocao:
        resposta = (
            self.cliente.table(NOME_TABELA_SOLICITACOES)
            .select("*")
            .eq("id", str(solicitacao_id))
            .execute()
        )
        if not resposta.data:
            raise RegraNegocioException("Solicitacao de adocao nao encontrada.")

        registro = resposta.data[0]
        return SolicitacaoAdocao(
            id=uuid.UUID(registro["id"]),
            animal_id=uuid.UUID(registro["animal_id"]),
            adotante_id=uuid.UUID(registro["adotante_id"]),
            status=StatusSolicitacao(registro["status"])
        )

    def recusar_outras_solicitacoes_do_animal(
        self,
        animal_id: uuid.UUID,
        solicitacao_aprovada_id: uuid.UUID,
        motivo_recusa: str
    ) -> None:
        # Nota Arquitetural do Blueprint: recusa automaticamente todas as demais solicitacoes
        # PENDENTES ou EM_ANALISE do mesmo animal quando uma solicitacao e aprovada.
        self.cliente.table(NOME_TABELA_SOLICITACOES) \
            .update({"status": StatusSolicitacao.RECUSADA.value}) \
            .eq("animal_id", str(animal_id)) \
            .neq("id", str(solicitacao_aprovada_id)) \
            .in_("status", [StatusSolicitacao.PENDENTE.value, StatusSolicitacao.EM_ANALISE.value]) \
            .execute()

    def listar_por_status(self, status: StatusSolicitacao) -> List[SolicitacaoParaAvaliacaoDTO]:
        resposta_solicitacoes = (
            self.cliente.table(NOME_TABELA_SOLICITACOES)
            .select("id, animal_id, adotante_id, status, animais(nome), usuarios(nome)")
            .eq("status", status.value)
            .execute()
        )

        if not resposta_solicitacoes.data:
            return []

        identificadores_adotantes = [
            registro["adotante_id"] for registro in resposta_solicitacoes.data
        ]
        resposta_questionarios = (
            self.cliente.table(NOME_TABELA_QUESTIONARIOS)
            .select("adotante_id, respostas")
            .in_("adotante_id", identificadores_adotantes)
            .execute()
        )

        mapa_respostas_por_adotante: Dict[str, Dict[str, str]] = {
            item["adotante_id"]: item.get("respostas") or {}
            for item in resposta_questionarios.data
        }

        return [
            SolicitacaoParaAvaliacaoDTO(
                id=uuid.UUID(registro["id"]),
                animal_id=uuid.UUID(registro["animal_id"]),
                animal_nome=(registro.get("animais") or {}).get("nome", ""),
                adotante_id=uuid.UUID(registro["adotante_id"]),
                adotante_nome=(registro.get("usuarios") or {}).get("nome", ""),
                status=registro["status"],
                respostas_triagem=mapa_respostas_por_adotante.get(registro["adotante_id"], {})
            )
            for registro in resposta_solicitacoes.data
        ]