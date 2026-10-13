import React from 'react';

// O componente isola a consistência visual de campos de seleção.
export const Select = ({ 
  label, 
  id, 
  options, 
  error, 
  ...props 
}) => {
  // Lei da Proximidade: Agrupamento da label e do campo via gap-1, idêntico ao Input.jsx
  return (
    <div className="flex flex-col gap-1 w-full">
      {label && (
        <label htmlFor={id} className="text-sm font-semibold text-textoDestaque">
          {label}
        </label>
      )}
      
      <select
        id={id}
        // Affordance: Borda e anel de foco explícitos para indicar interatividade por mouse ou teclado
        className={`
          w-full px-4 py-3 bg-white border rounded-lg text-textoCorpo appearance-none
          transition-colors duration-200 focus:outline-none focus:ring-2
          ${error 
            ? 'border-erro focus:ring-erro/50' 
            : 'border-borda focus:border-primaria focus:ring-primaria/30'
          }
          disabled:bg-fundo disabled:cursor-not-allowed
        `}
        aria-invalid={!!error}
        {...props}
      >
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
    </div>
  );
};