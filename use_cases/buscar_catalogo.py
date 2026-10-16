from typing import List, Optional
from use_cases.interfaces.animal_repository_interface import (
    AnimalRepositoryInterface,
    AnimalCatalogoDTO
)

PAGINA_INICIAL_PADRAO = 1
ITENS_POR_PAGINA_PADRAO = 20
DESLOCAMENTO_UNIDADE_PAGINA = 1


class BuscarCatalogo:
    def __init__(self, repositorio_animal: AnimalRepositoryInterface):
        self.repositorio_animal = repositorio_animal

    def executar(
        self,
        pagina: int = PAGINA_INICIAL_PADRAO,
        itens_por_pagina: int = ITENS_POR_PAGINA_PADRAO,
        nome: Optional[str] = None,
        porte: Optional[str] = None
    ) -> List[AnimalCatalogoDTO]:
        pagina_valida = max(pagina, PAGINA_INICIAL_PADRAO)
        deslocamento_registros = (pagina_valida - DESLOCAMENTO_UNIDADE_PAGINA) * itens_por_pagina

        return self.repositorio_animal.listar_disponiveis_paginados(
            limite=itens_por_pagina,
            deslocamento=deslocamento_registros,
            nome=nome,
            porte=porte
        )