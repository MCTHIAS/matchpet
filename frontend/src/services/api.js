// Isolamento da camada "Frameworks & Drivers" para requisições HTTP.
const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

export const httpClient = async (endpoint, options = {}) => {
  const defaultHeaders = {
    'Content-Type': 'application/json',
  };

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    ...options,
    headers: { ...defaultHeaders, ...options.headers },
  });

  if (!response.ok) {
    // A extração do erro deve ser tratada aqui para garantir que a UI
    // consuma uma exceção limpa e previsível para suas máquinas de estado.
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.message || `Erro HTTP: ${response.status}`);
  }

  // Respostas 204 (No Content) não devem tentar parsear JSON
  if (response.status === 204) {
    return null; 
  }

  return response.json();
};