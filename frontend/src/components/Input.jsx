import React from 'react';

// Componente base para formulários, como o Questionário de Triagem.
export const Input = ({ 
  label, 
  id, 
  error, 
  helperText, 
  ...props 
}) => {
  // Hierarquia Visual: Rótulos possuem peso visual maior que o texto de apoio
  // Lei da Proximidade: Gap pequeno (gap-1) agrupa a label, o input e a mensagem de erro
  return (
    <div className="flex flex-col gap-1 w-full">
      {label && (
        <label htmlFor={id} className="text-sm font-semibold text-textoDestaque">
          {label}
        </label>
      )}
      
      <input
        id={id}
        // Affordance: Borda visível que muda de cor ao receber foco, indicando claramente área editável
        className={`
          w-full px-4 py-3 bg-white border rounded-lg text-textoCorpo
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

      {/* Máquina de estados: Renderiza mensagem de erro ou texto de apoio garantindo contraste semântico */}
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