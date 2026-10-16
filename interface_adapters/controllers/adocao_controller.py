import uuid
from typing import Dict
from interface_adapters.http_context import IHttpContext
from use_cases.enviar_solicitacao_adocao import EnviarSolicitacaoAdocao
from use_cases.avaliar_solicitacao import AvaliarSolicitacao
from domain.exceptions import DominioException, ConcorrenciaSolicitacaoException

STATUS_HTTP_SUCESSO = 200
STATUS_HTTP_CRIADO = 201
STATUS_HTTP_REQUISICAO_INVALIDA = 400
STATUS_HTTP_CONFLITO_CONCORRENCIA = 409
STATUS_HTTP_ERRO_INTERNO = 500

DECISAO_STATUS_APROVADA = "APROVADA"
NOME_ADOTANTE_PADRAO = "Adotante Interessado"
DOMINIO_EMAIL_PADRAO = "@adotante.matchpet.org"


class AdocaoController:
    def __init__(
        self,
        caso_uso_enviar_solicitacao: EnviarSolicitacaoAdocao,
        caso_uso_avaliar_solicitacao: AvaliarSolicitacao
    ):
        self.caso_uso_enviar_solicitacao = caso_uso_enviar_solicitacao
        self.caso_uso_avaliar_solicitacao = caso_uso_avaliar_solicitacao

    def solicitar_adocao(self, contexto_http: IHttpContext) -> None:
        try:
            corpo_requisicao = contexto_http.obter_corpo()

            identificador_animal_bruto = (
                corpo_requisicao.get("animal_id") or corpo_requisicao.get("animalId")
            )
            animal_id = uuid.UUID(str(identificador_animal_bruto))

            identificador_adotante_bruto = (
                corpo_requisicao.get("adotante_id") or corpo_requisicao.get("adotanteId")
            )
            adotante_id = (
                uuid.UUID(str(identificador_adotante_bruto))
                if identificador_adotante_bruto
                else uuid.uuid4()
            )

            respostas_brutas = corpo_requisicao.get("respostas", {})
            respostas_questionario: Dict[str, str] = (
                {str(chave): str(valor) for chave, valor in respostas_brutas.items()}
                if isinstance(respostas_brutas, dict)
                else {}
            )

            nome_adotante = str(
                corpo_requisicao.get("nome")
                or respostas_questionario.get("nome")
                or respostas_questionario.get("nomeAdotante")
                or NOME_ADOTANTE_PADRAO
            )
            email_adotante = str(
                corpo_requisicao.get("email")
                or respostas_questionario.get("email")
                or f"{adotante_id}{DOMINIO_EMAIL_PADRAO}"
            )

            solicitacao_id = self.caso_uso_enviar_solicitacao.executar(
                animal_id=animal_id,
                adotante_id=adotante_id,
                nome_adotante=nome_adotante,
                email_adotante=email_adotante,
                respostas_questionario=respostas_questionario
            )

            contexto_http.responder(
                STATUS_HTTP_CRIADO,
                {"id": str(solicitacao_id), "solicitacao_id": str(solicitacao_id)}
            )

        except DominioException as erro_dominio:
            contexto_http.responder(STATUS_HTTP_REQUISICAO_INVALIDA, {"message": str(erro_dominio)})
        except (ValueError, TypeError):
            contexto_http.responder(
                STATUS_HTTP_REQUISICAO_INVALIDA,
                {"message": "Identificador do animal ou do adotante em formato UUID invalido."}
            )
        except Exception as erro_infraestrutura:
            contexto_http.responder(
                STATUS_HTTP_ERRO_INTERNO,
                {"message": f"Falha ao registar solicitacao de adocao: {str(erro_infraestrutura)}"}
            )

    def listar_pendentes(self, contexto_http: IHttpContext) -> None:
        try:
            solicitacoes_pendentes = self.caso_uso_avaliar_solicitacao.listar_pendentes()
            lista_formatada = [
                {
                    "id": str(solicitacao.id),
                    "animal_id": str(solicitacao.animal_id),
                    "animalId": str(solicitacao.animal_id),
                    "animal_nome": solicitacao.animal_nome,
                    "animal": {"id": str(solicitacao.animal_id), "nome": solicitacao.animal_nome},
                    "adotante_id": str(solicitacao.adotante_id),
                    "adotante_nome": solicitacao.adotante_nome,
                    "adotante": {"id": str(solicitacao.adotante_id), "nome": solicitacao.adotante_nome},
                    "status": solicitacao.status,
                    "respostas": solicitacao.respostas_triagem
                }
                for solicitacao in solicitacoes_pendentes
            ]
            contexto_http.responder(STATUS_HTTP_SUCESSO, lista_formatada)
        except Exception as erro_infraestrutura:
            contexto_http.responder(
                STATUS_HTTP_ERRO_INTERNO,
                {"message": f"Erro ao listar solicitacoes pendentes: {str(erro_infraestrutura)}"}
            )

    def avaliar(self, contexto_http: IHttpContext, solicitacao_id_texto: str) -> None:
        try:
            corpo_requisicao = contexto_http.obter_corpo()
            status_decisao = corpo_requisicao.get("status")

            if status_decisao is not None:
                aprovar_solicitacao = str(status_decisao).upper() == DECISAO_STATUS_APROVADA
            else:
                aprovar_solicitacao = bool(corpo_requisicao.get("aprovar"))

            self.caso_uso_avaliar_solicitacao.executar(
                solicitacao_id=uuid.UUID(solicitacao_id_texto),
                aprovar=aprovar_solicitacao
            )
            contexto_http.responder(
                STATUS_HTTP_SUCESSO,
                {"message": "Avaliacao processada com sucesso."}
            )
        except ConcorrenciaSolicitacaoException as erro_concorrencia:
            contexto_http.responder(STATUS_HTTP_CONFLITO_CONCORRENCIA, {"message": str(erro_concorrencia)})
        except DominioException as erro_dominio:
            contexto_http.responder(STATUS_HTTP_REQUISICAO_INVALIDA, {"message": str(erro_dominio)})
        except (ValueError, TypeError):
            contexto_http.responder(
                STATUS_HTTP_REQUISICAO_INVALIDA,
                {"message": "Identificador da solicitacao invalido."}
            )
        except Exception as erro_infraestrutura:
            contexto_http.responder(
                STATUS_HTTP_ERRO_INTERNO,
                {"message": f"Erro ao avaliar solicitacao: {str(erro_infraestrutura)}"}
            )