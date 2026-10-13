from typing import List
from use_cases.interfaces.animal_repository_interface import AnimalRepositoryInterface
from use_cases.dtos import AnimalCatalogoDTO

class BuscarCatalogo:
    def __init__(self, animal_repository: AnimalRepositoryInterface):
        self.animal_repository = animal_repository

    def executar(self, pagina: int = 1, itens_por_pagina: int = 20) -> List[AnimalCatalogoDTO]:
        # Delega ao repositório a responsabilidade de construir DTOs leves
        # para mitigar a latência de mapeamento e overhead de memória.
        offset = (pagina - 1) * itens_por_pagina
        return self.animal_repository.listar_animais_paginados(limite=itens_por_pagina, offset=offset)