import React from 'react';

// Componente para respostas extensas do Questionário de Triagem.
export const Textarea = ({ 
  label, 
  id, 
  error, 
  helperText, 
  rows = 4,
  ...props 
}) => {
  // Lei da Proximidade: Agrupamento coerente entre label, campo e mensagens
  return (
    <div className="flex flex-col gap-1 w-full">
      {label && (
        <label htmlFor={id} className="text-sm font-semibold text-textoDestaque">
          {label}
        </label>
      )}
      
      <textarea
        id={id}
        rows={rows}
        // Affordance: Borda visível, anel de foco e permissão de redimensionamento vertical
        className={`
          w-full px-4 py-3 bg-white border rounded-lg text-textoCorpo resize-y
          transition-colors duration-200 focus:outline-none focus:ring-2
          ${error 
            ? 'border-erro focus:ring-erro/50' 
            : 'border-borda focus:border-primaria focus:ring-primaria/30'
          }
          disabled:bg-fundo disabled:cursor-not-allowed
        `}
        aria-invalid={!!error}
        aria-describedby={error ? `${id}-error` : helperText ? `${id}-helper` : undefined}
        {...props}
      />

      {error ? (
        <span id={`${id}-error`} className="text-xs text-erro font-medium">
          {error}
        </span>
      ) : helperText ? (
        <span id={`${id}-helper`} className="text-xs text-textoApoio">
          {helperText}
        </span>
      ) : null}
    </div>
  );
};