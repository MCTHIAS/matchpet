import uuid
from typing import List
from domain.entities import Animal, StatusAnimal
from use_cases.interfaces.animal_repository_interface import AnimalRepositoryInterface

class CadastrarAnimal:
    def __init__(self, animal_repository: AnimalRepositoryInterface):
        self.animal_repository = animal_repository

    def executar(self, protetor_id: uuid.UUID, nome: str, porte: str, tags: List[str]) -> uuid.UUID:
        novo_animal = Animal(
            id=uuid.uuid4(),
            protetor_id=protetor_id,
            nome=nome,
            porte=porte,
            tags=tags,
            status=StatusAnimal.DISPONIVEL
        )
        self.animal_repository.salvar(novo_animal)
        return novo_animal.id