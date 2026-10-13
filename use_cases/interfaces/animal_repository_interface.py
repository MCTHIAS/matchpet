from abc import ABC, abstractmethod
import uuid
from typing import List
from domain.entities import Animal
from use_cases.dtos import AnimalCatalogoDTO

class AnimalRepositoryInterface(ABC):
    
    @abstractmethod
    def salvar(self, animal: Animal) -> None:
        pass
        
    @abstractmethod
    def buscar_por_id(self, id: uuid.UUID) -> Animal:
        pass

    @abstractmethod
    def listar_animais_paginados(self, limite: int, offset: int) -> List[AnimalCatalogoDTO]:
        """Retorna DTOs diretamente da fonte de dados para otimização de performance."""
        pass