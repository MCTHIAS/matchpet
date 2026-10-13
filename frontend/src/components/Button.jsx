import React from 'react';

// O botão gerencia seus próprios estados de interatividade e feedback assíncrono.
export const Button = ({ 
  children, 
  onClick, 
  variante = 'primaria', 
  isLoading = false, 
  disabled = false,
  type = 'button',
  fullWidth = false
}) => {
  // Previne interações concorrentes se a UI já estiver aguardando uma resposta
  const isActionDisabled = disabled || isLoading;

  const estilosVariante = {
    primaria: 'bg-primaria text-textoDestaque font-bold hover:brightness-95',
    secundaria: 'bg-transparent border-2 border-secundaria text-secundaria font-bold hover:bg-secundaria hover:text-fundo',
    alerta: 'bg-erro text-white font-bold hover:brightness-95'
  };

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={isActionDisabled}
      // Affordance: focus-visible garante anel de foco para navegação por teclado sem prejudicar usuários de mouse
      className={`
        relative flex justify-center items-center gap-2 py-3 px-6 rounded-lg 
        transition-all duration-200 ease-in-out focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-primaria
        ${estilosVariante[variante]}
        ${isActionDisabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer active:scale-95'}
        ${fullWidth ? 'w-full' : 'w-auto'}
      `}
      aria-disabled={isActionDisabled}
    >
      {/* Máquina de Estados: Feedback visual unificado bloqueando o texto original durante carregamento */}
      {isLoading ? (
        <span className="w-5 h-5 border-2 border-current border-t-transparent rounded-full animate-spin" aria-hidden="true" />
      ) : children}
    </button>
  );
};