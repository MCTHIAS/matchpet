import React from 'react';
import { ANIMAL_STATUS_UI } from '../theme/domainStates';

// Componente puramente visual que materializa o estado do ciclo de vida do animal.
// Aplica a regra de Máquina de Estados UI/UX baseada no domínio.
export const AnimalBadge = ({ status }) => {
  const config = ANIMAL_STATUS_UI[status];

  // Prevenção de erro caso o status vindo da API não exista no mapa local
  if (!config) return null;

  return (
    <span 
      className={`px-3 py-1 text-xs font-bold rounded-full ${config.corFundo} ${config.corTexto}`}
    >
      {config.label}
    </span>
  );
};