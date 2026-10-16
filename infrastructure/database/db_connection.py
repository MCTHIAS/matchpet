import os
from supabase import create_client, Client

VARIAVEL_AMBIENTE_URL_SUPABASE = "SUPABASE_URL"
VARIAVEL_AMBIENTE_CHAVE_SUPABASE = "SUPABASE_KEY"


def criar_cliente_banco_dados() -> Client:
    """
    Centraliza a criacao do driver de banco de dados na camada de Frameworks & Drivers,
    validando as credenciais antes de injeta-las nos repositorios.
    """
    url_conexao = os.environ.get(VARIAVEL_AMBIENTE_URL_SUPABASE, "").strip()
    chave_acesso = os.environ.get(VARIAVEL_AMBIENTE_CHAVE_SUPABASE, "").strip()

    if not url_conexao or not chave_acesso:
        raise RuntimeError(
            f"Credenciais ausentes: defina {VARIAVEL_AMBIENTE_URL_SUPABASE} e "
            f"{VARIAVEL_AMBIENTE_CHAVE_SUPABASE} no ficheiro .env na raiz do projeto."
        )

    return create_client(url_conexao, chave_acesso)