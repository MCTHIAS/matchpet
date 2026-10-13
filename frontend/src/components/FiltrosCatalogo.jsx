import React, { useState } from 'react';
import { Input } from './Input';
import { Select } from './Select';
import { Button } from './Button';

export const FiltrosCatalogo = ({ onFiltrar, isLoading }) => {
  const [nome, setNome] = useState('');
  const [porte, setPorte] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // A delegação da busca garante que o componente visual não conheça regras de rede (Clean Architecture)
    onFiltrar({ nome, porte });
  };

  const opcoesPorte = [
    { value: '', label: 'Todos os portes' },
    { value: 'PEQUENO', label: 'Pequeno' },
    { value: 'MEDIO', label: 'Médio' },
    { value: 'GRANDE', label: 'Grande' }
  ];

  // Mobile First: Os campos empilham-se verticalmente no mobile (flex-col) 
  // e alinham-se lado a lado a partir de telas médias (md:flex-row)
  // Lei da Proximidade: O formulário é contido em um card (bg-white, border) para separá-lo da listagem de animais.
  return (
    <form 
      onSubmit={handleSubmit} 
      className="bg-white p-5 rounded-xl border border-borda shadow-sm flex flex-col md:flex-row gap-4 items-end mb-6"
    >
      <div className="w-full md:flex-1">
        <Input 
          id="busca-nome"
          label="Buscar por nome"
          placeholder="Ex: Rex, Luna..."
          value={nome}
          onChange={(e) => setNome(e.target.value)}
          disabled={isLoading}
        />
      </div>
      
      <div className="w-full md:w-48">
        <Select 
          id="filtro-porte"
          label="Porte"
          options={opcoesPorte}
          value={porte}
          onChange={(e) => setPorte(e.target.value)}
          disabled={isLoading}
        />
      </div>

      <div className="w-full md:w-auto">
        <Button 
          type="submit" 
          isLoading={isLoading} 
          fullWidth
        >
          Filtrar
        </Button>
      </div>
    </form>
  );
};