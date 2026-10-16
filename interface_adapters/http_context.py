from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple, Optional


class IHttpContext(ABC):
    """
    Contrato que abstrai o protocolo HTTP para os Controllers,
    evitando acoplamento direto com o framework Flask (Regra da Dependencia).
    """
    @abstractmethod
    def obter_corpo(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def obter_parametro_consulta(self, chave: str, valor_padrao: Any = None) -> Any:
        pass

    @abstractmethod
    def obter_arquivo(self, chave: str) -> Tuple[Optional[bytes], Optional[str], Optional[str]]:
        pass

    @abstractmethod
    def responder(self, codigo_status: int, dados_resposta: Any) -> None:
        pass