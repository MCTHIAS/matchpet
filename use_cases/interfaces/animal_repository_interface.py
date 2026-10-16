from abc import ABC, abstractmethod
from dataclasses import dataclass
import uuid
from typing import List, Optional
from domain.entities import Animal


@dataclass(frozen=True)
class AnimalCatalogoDTO:
    """Estrutura de leitura enxuta para evitar hidratacao desnecessaria de entidades na listagem."""
    id: uuid.UUID
    nome: str
    porte: str
    tags: List[str]
    foto_url: Optional[str]


class AnimalRepositoryInterface(ABC):
    @abstractmethod
    def salvar(self, animal: Animal) -> None:
        pass

    @abstractmethod
    def buscar_por_id(self, animal_id: uuid.UUID) -> Animal:
        pass

    @abstractmethod
    def listar_disponiveis_paginados(
        self,
        limite: int,
        deslocamento: int,
        nome: Optional[str] = None,
        porte: Optional[str] = None
    ) -> List[AnimalCatalogoDTO]:
        pass