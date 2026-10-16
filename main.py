from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from infrastructure.database.db_connection import criar_cliente_banco_dados
from infrastructure.api.flask_routes import configurar_rotas

from interface_adapters.gateways.supabase_animal_repository import SupabaseAnimalRepository
from interface_adapters.gateways.supabase_solicitacao_repository import SupabaseSolicitacaoRepository
from interface_adapters.gateways.vercel_blob_storage_adapter import VercelBlobStorageAdapter

from use_cases.cadastrar_animal import CadastrarAnimal
from use_cases.buscar_catalogo import BuscarCatalogo
from use_cases.enviar_solicitacao_adocao import EnviarSolicitacaoAdocao
from use_cases.avaliar_solicitacao import AvaliarSolicitacao

from interface_adapters.controllers.animal_controller import AnimalController
from interface_adapters.controllers.adocao_controller import AdocaoController

ENDERECO_HOST_PADRAO = "0.0.0.0"
PORTA_SERVIDOR_PADRAO = 5000
MODO_DEPURACAO_ATIVO = True


def criar_aplicacao() -> Flask:
    """
    Atua como Raiz de Composicao (Composition Root), instanciando os drivers
    da camada mais externa (Frameworks & Drivers) e injetando os adaptadores
    nos casos de uso para cumprir a Inversao de Dependencia.
    """
    load_dotenv()

    aplicacao_web = Flask(__name__)
    CORS(aplicacao_web)

    # Regra arquitetural: a conexao com o PostgreSQL/Supabase nasce na camada de infraestrutura
    # e e injetada via construtor nos repositorios, evitando acoplamento oculto.
    cliente_supabase = criar_cliente_banco_dados()

    repositorio_animal = SupabaseAnimalRepository(cliente_supabase)
    repositorio_solicitacao = SupabaseSolicitacaoRepository(cliente_supabase)
    servico_armazenamento = VercelBlobStorageAdapter()

    # Regra da Dependencia: os casos de uso conhecem apenas os contratos (interfaces)
    # e recebem as implementacoes concretas injetadas de fora para dentro.
    caso_uso_cadastrar_animal = CadastrarAnimal(repositorio_animal, servico_armazenamento)
    caso_uso_buscar_catalogo = BuscarCatalogo(repositorio_animal)
    caso_uso_enviar_solicitacao = EnviarSolicitacaoAdocao(repositorio_solicitacao, repositorio_animal)
    caso_uso_avaliar_solicitacao = AvaliarSolicitacao(repositorio_solicitacao, repositorio_animal)

    controlador_animal = AnimalController(caso_uso_cadastrar_animal, caso_uso_buscar_catalogo)
    controlador_adocao = AdocaoController(
        caso_uso_enviar_solicitacao,
        caso_uso_avaliar_solicitacao
    )

    configurar_rotas(aplicacao_web, controlador_animal, controlador_adocao)

    return aplicacao_web


if __name__ == "__main__":
    servidor_aplicacao = criar_aplicacao()
    servidor_aplicacao.run(
        host=ENDERECO_HOST_PADRAO,
        port=PORTA_SERVIDOR_PADRAO,
        debug=MODO_DEPURACAO_ATIVO
    )