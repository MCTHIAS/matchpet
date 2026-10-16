import uuid
from typing import List, Optional
from supabase import Client
from domain.entities import Animal, StatusAnimal
from domain.exceptions import RegraNegocioException
from use_cases.interfaces.animal_repository_interface import (
    AnimalRepositoryInterface,
    AnimalCatalogoDTO
)

NOME_TABELA_ANIMAIS = "animais"
NOME_TABELA_USUARIOS = "usuarios"
NOME_PROTETOR_PADRAO = "Protetor Responsavel"
PAPEL_USUARIO_PROTETOR = "PROTETOR"
DOMINIO_EMAIL_PROTETOR = "@protetor.matchpet.org"
DESLOCAMENTO_INDICE_FINAL = 1


class SupabaseAnimalRepository(AnimalRepositoryInterface):
    def __init__(self, cliente_supabase: Client):
        self.cliente = cliente_supabase

    def _garantir_existencia_protetor(self, protetor_id: uuid.UUID) -> None:
        # Regra de integridade relacional: a tabela animais exige chave estrangeira em usuarios(id).
        consulta_usuario = (
            self.cliente.table(NOME_TABELA_USUARIOS)
            .select("id")
            .eq("id", str(protetor_id))
            .execute()
        )
        if not consulta_usuario.data:
            dados_protetor = {
                "id": str(protetor_id),
                "nome": NOME_PROTETOR_PADRAO,
                "papel": PAPEL_USUARIO_PROTETOR,
                "email": f"{protetor_id}{DOMINIO_EMAIL_PROTETOR}"
            }
            self.cliente.table(NOME_TABELA_USUARIOS).upsert(dados_protetor).execute()

    def salvar(self, animal: Animal) -> None:
        self._garantir_existencia_protetor(animal.protetor_id)

        dados_persistencia = {
            "id": str(animal.id),
            "protetor_id": str(animal.protetor_id),
            "nome": animal.nome,
            "porte": animal.porte,
            "tags": animal.tags,
            "status": animal.status.value,
            "foto_url": animal.foto_url
        }
        self.cliente.table(NOME_TABELA_ANIMAIS).upsert(dados_persistencia).execute()

    def buscar_por_id(self, animal_id: uuid.UUID) -> Animal:
        resposta = (
            self.cliente.table(NOME_TABELA_ANIMAIS)
            .select("*")
            .eq("id", str(animal_id))
            .execute()
        )
        if not resposta.data:
            raise RegraNegocioException("Animal nao encontrado no registo.")

        registro = resposta.data[0]
        return Animal(
            id=uuid.UUID(registro["id"]),
            protetor_id=uuid.UUID(registro["protetor_id"]),
            nome=registro["nome"],
            porte=registro["porte"],
            tags=registro.get("tags") or [],
            status=StatusAnimal(registro["status"]),
            foto_url=registro.get("foto_url")
        )

    def listar_disponiveis_paginados(
        self,
        limite: int,
        deslocamento: int,
        nome: Optional[str] = None,
        porte: Optional[str] = None
    ) -> List[AnimalCatalogoDTO]:
        # Regra: apenas animais com status DISPONIVEL aparecem no catalogo publico.
        consulta = (
            self.cliente.table(NOME_TABELA_ANIMAIS)
            .select("id, nome, porte, tags, foto_url")
            .eq("status", StatusAnimal.DISPONIVEL.value)
        )

        if nome and nome.strip():
            consulta = consulta.ilike("nome", f"%{nome.strip()}%")
        if porte and porte.strip():
            consulta = consulta.eq("porte", porte.strip())

        indice_final = deslocamento + limite - DESLOCAMENTO_INDICE_FINAL
        resposta = consulta.range(deslocamento, indice_final).execute()

        return [
            AnimalCatalogoDTO(
                id=uuid.UUID(registro["id"]),
                nome=registro["nome"],
                porte=registro["porte"],
                tags=registro.get("tags") or [],
                foto_url=registro.get("foto_url")
            )
            for registro in resposta.data
        ]