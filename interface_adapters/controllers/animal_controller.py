import os
import uuid
from typing import List
from interface_adapters.http_context import IHttpContext
from interface_adapters.presenters.animal_presenter import AnimalPresenter
from use_cases.cadastrar_animal import CadastrarAnimal
from use_cases.buscar_catalogo import BuscarCatalogo
from domain.exceptions import DominioException

STATUS_HTTP_SUCESSO = 200
STATUS_HTTP_CRIADO = 201
STATUS_HTTP_REQUISICAO_INVALIDA = 400
STATUS_HTTP_ERRO_INTERNO = 500

PAGINA_INICIAL_PADRAO = 1
ITENS_POR_PAGINA_PADRAO = 20
PROTETOR_PADRAO_ID_FALLBACK = "00000000-0000-0000-0000-000000000001"
VARIAVEL_AMBIENTE_PROTETOR_PADRAO = "PROTETOR_PADRAO_ID"


class AnimalController:
    def __init__(
        self,
        caso_uso_cadastrar_animal: CadastrarAnimal,
        caso_uso_buscar_catalogo: BuscarCatalogo
    ):
        self.caso_uso_cadastrar_animal = caso_uso_cadastrar_animal
        self.caso_uso_buscar_catalogo = caso_uso_buscar_catalogo

    def cadastrar(self, contexto_http: IHttpContext) -> None:
        try:
            corpo_requisicao = contexto_http.obter_corpo()
            foto_binario, foto_nome, tipo_conteudo_foto = contexto_http.obter_arquivo("foto")

            # Regra: como a interface publica do MVP nao exige login na tela de resgate,
            # utiliza o identificador de protetor configurado no ambiente caso nao venha no formulario.
            identificador_protetor_bruto = (
                corpo_requisicao.get("protetor_id")
                or os.environ.get(VARIAVEL_AMBIENTE_PROTETOR_PADRAO, PROTETOR_PADRAO_ID_FALLBACK)
            )
            protetor_id = uuid.UUID(str(identificador_protetor_bruto))

            tags_recebidas = corpo_requisicao.get("tags", "")
            lista_tags: List[str] = (
                [item.strip() for item in str(tags_recebidas).split(",") if item.strip()]
                if isinstance(tags_recebidas, str)
                else list(tags_recebidas)
            )

            identificador_animal = self.caso_uso_cadastrar_animal.executar(
                protetor_id=protetor_id,
                nome=str(corpo_requisicao.get("nome", "")),
                porte=str(corpo_requisicao.get("porte", "")),
                tags=lista_tags,
                foto_binario=foto_binario,
                foto_nome=foto_nome,
                tipo_conteudo_foto=tipo_conteudo_foto or ""
            )

            resposta_apresentacao = AnimalPresenter.formatar_cadastro(identificador_animal)
            contexto_http.responder(STATUS_HTTP_CRIADO, resposta_apresentacao)

        except DominioException as erro_dominio:
            contexto_http.responder(STATUS_HTTP_REQUISICAO_INVALIDA, {"message": str(erro_dominio)})
        except (ValueError, TypeError):
            contexto_http.responder(
                STATUS_HTTP_REQUISICAO_INVALIDA,
                {"message": "Identificador do protetor em formato UUID invalido."}
            )
        except Exception as erro_infraestrutura:
            contexto_http.responder(
                STATUS_HTTP_ERRO_INTERNO,
                {"message": f"Falha ao registar animal: {str(erro_infraestrutura)}"}
            )

    def listar_catalogo(self, contexto_http: IHttpContext) -> None:
        try:
            pagina = int(contexto_http.obter_parametro_consulta("pagina", PAGINA_INICIAL_PADRAO))
            itens_por_pagina = int(contexto_http.obter_parametro_consulta("itens", ITENS_POR_PAGINA_PADRAO))
            filtro_nome = contexto_http.obter_parametro_consulta("nome")
            filtro_porte = contexto_http.obter_parametro_consulta("porte")

            animais_encontrados = self.caso_uso_buscar_catalogo.executar(
                pagina=pagina,
                itens_por_pagina=itens_por_pagina,
                nome=filtro_nome,
                porte=filtro_porte
            )
            resposta_formatada = AnimalPresenter.formatar_catalogo(animais_encontrados)
            contexto_http.responder(STATUS_HTTP_SUCESSO, resposta_formatada)

        except (ValueError, TypeError):
            contexto_http.responder(
                STATUS_HTTP_REQUISICAO_INVALIDA,
                {"message": "Parametros de paginacao invalidos."}
            )
        except Exception as erro_infraestrutura:
            contexto_http.responder(
                STATUS_HTTP_ERRO_INTERNO,
                {"message": f"Falha ao listar catalogo: {str(erro_infraestrutura)}"}
            )