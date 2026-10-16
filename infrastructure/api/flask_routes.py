from flask import Flask
from infrastructure.api.flask_adapter import FlaskAdapter
from interface_adapters.controllers.animal_controller import AnimalController
from interface_adapters.controllers.adocao_controller import AdocaoController


def configurar_rotas(
    aplicacao: Flask,
    controlador_animal: AnimalController,
    controlador_adocao: AdocaoController
) -> None:

    @aplicacao.route("/api/animais", methods=["POST"])
    def rota_cadastrar_animal():
        adaptador_http = FlaskAdapter()
        controlador_animal.cadastrar(adaptador_http)
        return adaptador_http.gerar_resposta()

    @aplicacao.route("/api/animais", methods=["GET"])
    def rota_listar_catalogo():
        adaptador_http = FlaskAdapter()
        controlador_animal.listar_catalogo(adaptador_http)
        return adaptador_http.gerar_resposta()

    @aplicacao.route("/api/solicitacoes", methods=["POST"])
    @aplicacao.route("/api/adocao/solicitar", methods=["POST"])
    def rota_solicitar_adocao():
        adaptador_http = FlaskAdapter()
        controlador_adocao.solicitar_adocao(adaptador_http)
        return adaptador_http.gerar_resposta()

    @aplicacao.route("/api/solicitacoes", methods=["GET"])
    def rota_listar_solicitacoes():
        adaptador_http = FlaskAdapter()
        controlador_adocao.listar_pendentes(adaptador_http)
        return adaptador_http.gerar_resposta()

    @aplicacao.route("/api/solicitacoes/<solicitacao_id>/avaliar", methods=["POST"])
    def rota_avaliar_solicitacao(solicitacao_id: str):
        adaptador_http = FlaskAdapter()
        controlador_adocao.avaliar(adaptador_http, solicitacao_id)
        return adaptador_http.gerar_resposta()