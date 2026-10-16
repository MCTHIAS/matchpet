import os
import json
import urllib.parse
import urllib.request
import urllib.error
from use_cases.interfaces.storage_service_interface import StorageServiceInterface

VARIAVEL_AMBIENTE_TOKEN_BLOB = "BLOB_READ_WRITE_TOKEN"
URL_BASE_VERCEL_BLOB = "https://blob.vercel-storage.com"
VERSAO_API_VERCEL_BLOB = "7"
TIPO_CONTEUDO_BINARIO_PADRAO = "application/octet-stream"


class VercelBlobStorageAdapter(StorageServiceInterface):
    def __init__(self):
        self.token_acesso = os.environ.get(VARIAVEL_AMBIENTE_TOKEN_BLOB, "").strip()

    def enviar_arquivo(
        self,
        nome_arquivo: str,
        conteudo_binario: bytes,
        tipo_conteudo: str
    ) -> str:
        if not self.token_acesso:
            raise RuntimeError(
                f"Variavel de ambiente {VARIAVEL_AMBIENTE_TOKEN_BLOB} nao configurada no ficheiro .env."
            )

        nome_arquivo_seguro = urllib.parse.quote(nome_arquivo)
        url_destino = f"{URL_BASE_VERCEL_BLOB}/{nome_arquivo_seguro}"
        cabecalhos = {
            "authorization": f"Bearer {self.token_acesso}",
            "content-type": tipo_conteudo or TIPO_CONTEUDO_BINARIO_PADRAO,
            "x-api-version": VERSAO_API_VERCEL_BLOB
        }

        requisicao = urllib.request.Request(
            url_destino,
            data=conteudo_binario,
            headers=cabecalhos,
            method="PUT"
        )
        try:
            with urllib.request.urlopen(requisicao) as resposta_http:
                corpo_json = json.loads(resposta_http.read().decode("utf-8"))
                return str(corpo_json.get("url", ""))
        except urllib.error.HTTPError as erro_http:
            detalhe_erro = erro_http.read().decode("utf-8", errors="ignore")
            raise RuntimeError(
                f"Erro HTTP {erro_http.code} no upload para o Vercel Blob: {detalhe_erro}"
            ) from erro_http
        except urllib.error.URLError as erro_rede:
            raise RuntimeError(
                f"Falha de comunicacao com o Vercel Blob: {str(erro_rede)}"
            ) from erro_rede