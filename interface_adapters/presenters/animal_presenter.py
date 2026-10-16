from typing import List, Dict, Any
from use_cases.interfaces.animal_repository_interface import AnimalCatalogoDTO


class AnimalPresenter:
    @staticmethod
    def formatar_catalogo(animais_catalogo: List[AnimalCatalogoDTO]) -> List[Dict[str, Any]]:
        # Regra: serializa tipos de dominio (UUID) em tipos primitivos para consumo pelo React.
        return [
            {
                "id": str(animal.id),
                "nome": animal.nome,
                "porte": animal.porte,
                "tags": animal.tags,
                "foto_url": animal.foto_url
            }
            for animal in animais_catalogo
        ]

    @staticmethod
    def formatar_cadastro(identificador_animal: Any) -> Dict[str, str]:
        return {"id": str(identificador_animal)}