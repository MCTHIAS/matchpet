from abc import ABC, abstractmethod


class StorageServiceInterface(ABC):
    @abstractmethod
    def enviar_arquivo(
        self,
        nome_arquivo: str,
        conteudo_binario: bytes,
        tipo_conteudo: str
    ) -> str:
        pass