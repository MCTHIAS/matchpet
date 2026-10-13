from dataclasses import dataclass
import uuid
from typing import List

@dataclass(frozen=True)
class AnimalCatalogoDTO:
    """DTO enxuto para evitar overhead de memória nas buscas de leitura do catálogo."""
    id: uuid.UUID
    nome: str
    porte: str
    tags: List[str]
    foto_url: str