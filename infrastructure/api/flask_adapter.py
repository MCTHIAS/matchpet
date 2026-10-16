from typing import Any, Dict, Tuple, Optional
from flask import request, jsonify, Response
from interface_adapters.http_context import IHttpContext

STATUS_HTTP_PADRAO = 200


class FlaskAdapter(IHttpContext):
    def __init__(self):
        self.dados_resposta: Any = None
        self.codigo_status: int = STATUS_HTTP_PADRAO

    def obter_corpo(self) -> Dict[str, Any]:
        # Regra: abstrai a diferenca entre payloads JSON e multipart/form-data para os Controllers.
        if request.is_json:
            return request.get_json(silent=True) or {}
        return request.form.to_dict()

    def obter_parametro_consulta(self, chave: str, valor_padrao: Any = None) -> Any:
        return request.args.get(chave, valor_padrao)

    def obter_arquivo(self, chave: str) -> Tuple[Optional[bytes], Optional[str], Optional[str]]:
        arquivo_enviado = request.files.get(chave)
        if arquivo_enviado and arquivo_enviado.filename:
            return arquivo_enviado.read(), arquivo_enviado.filename, arquivo_enviado.content_type
        return None, None, None

    def responder(self, codigo_status: int, dados_resposta: Any) -> None:
        self.codigo_status = codigo_status
        self.dados_resposta = dados_resposta

    def gerar_resposta(self) -> Tuple[Response, int]:
        return jsonify(self.dados_resposta), self.codigo_status