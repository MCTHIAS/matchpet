import { fetchApi } from "./api";

const PROTETOR_PADRAO_ID = "00000000-0000-0000-0000-000000000001";

export async function buscarCatalogo({ pagina = 1, itens = 20, nome = "", porte = "" } = {}) {
  // Filtra parâmetros vazios antes de montar a URL para evitar queries poluídas no backend.
  const queryParams = new URLSearchParams({
    pagina: pagina.toString(),
    itens: itens.toString(),
  });

  if (nome) queryParams.append("nome", nome);
  if (porte) queryParams.append("porte", porte);

  return fetchApi(`/animais?${queryParams.toString()}`);
}

export async function cadastrarAnimal(dadosAnimal, arquivoFoto) {
  const formData = new FormData();

  formData.append("nome", dadosAnimal.nome);
  formData.append("porte", dadosAnimal.porte);
  formData.append("tags", dadosAnimal.tags || "");
  // Garante o vínculo de responsabilidade exigido pela entidade Animal mesmo sem tela de login no MVP.
  formData.append("protetor_id", dadosAnimal.protetor_id || PROTETOR_PADRAO_ID);

  if (arquivoFoto) {
    formData.append("foto", arquivoFoto);
  }

  return fetchApi("/animais", {
    method: "POST",
    body: formData,
  });
}