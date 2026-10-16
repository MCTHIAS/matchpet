import uuid
from typing import List, Optional
from domain.entities import Animal, StatusAnimal
from use_cases.interfaces.animal_repository_interface import AnimalRepositoryInterface
from use_cases.interfaces.storage_service_interface import StorageServiceInterface


class CadastrarAnimal:
    def __init__(
        self,
        repositorio_animal: AnimalRepositoryInterface,
        servico_armazenamento: StorageServiceInterface
    ):
        self.repositorio_animal = repositorio_animal
        self.servico_armazenamento = servico_armazenamento

    def executar(
        self,
        protetor_id: uuid.UUID,
        nome: str,
        porte: str,
        tags: List[str],
        foto_binario: Optional[bytes] = None,
        foto_nome: Optional[str] = None,
        tipo_conteudo_foto: str = ""
    ) -> uuid.UUID:
        url_foto_armazenada: Optional[str] = None
        if foto_binario and foto_nome:
            url_foto_armazenada = self.servico_armazenamento.enviar_arquivo(
                nome_arquivo=foto_nome,
                conteudo_binario=foto_binario,
                tipo_conteudo=tipo_conteudo_foto
            )

        novo_animal = Animal(
            id=uuid.uuid4(),
            protetor_id=protetor_id,
            nome=nome,
            porte=porte,
            tags=tags,
            status=StatusAnimal.DISPONIVEL,
            foto_url=url_foto_armazenada
        )

        self.repositorio_animal.salvar(novo_animal)
        return novo_animal.id