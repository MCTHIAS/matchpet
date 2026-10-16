// Isolamento da camada de infraestrutura HTTP para que os componentes visuais 
// dependam apenas de contratos abstratos de serviço, respeitando a Regra da Dependência.
const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:5000/api";

export async function fetchApi(endpoint, options = {}) {
  const config = { ...options };
  const headers = { ...config.headers };

  // Quando o corpo é FormData (upload de imagem), o navegador precisa omitir o Content-Type 
  // manual para calcular e injetar automaticamente o boundary do multipart/form-data.
  if (!(config.body instanceof FormData)) {
    headers["Content-Type"] = headers["Content-Type"] || "application/json";
  }

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    ...config,
    headers,
  });

  if (!response.ok) {
    // Padroniza a captura de exceções de domínio vindas da API para alimentar a Máquina de Estados da UI.
    const erroJson = await response.json().catch(() => ({}));
    throw new Error(erroJson.message || "Erro na comunicacao com o servidor.");
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

// Mantido como alias para retrocompatibilidade caso algum componente auxiliar ainda referencie httpClient.
export const httpClient = fetchApi;