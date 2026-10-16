from dataclasses import dataclass
import uuid
from typing import List, Dict, Optional

@dataclass(frozen=True)
class AnimalCatalogoDTO:
    id: uuid.UUID
    nome: str
    porte: str
    tags: List[str]
    foto_url: Optional[str]

@dataclass(frozen=True)
class SolicitacaoPendenteDTO:
    """
    DTO desenhado especificamente para compor os dados aninhados do painel de avaliação.
    Evita que a UI precise fazer requisições adicionais para buscar dados do animal e adotante.
    """
    id: uuid.UUID
    animal_id: uuid.UUID
    animal_nome: str
    adotante_id: uuid.UUID
    adotante_nome: str
    respostas_triagem: Dict[str, str]