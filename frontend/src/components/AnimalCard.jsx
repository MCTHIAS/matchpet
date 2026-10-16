import React from "react";
import { Button } from "./Button";

export const AnimalCard = ({ animal, onClickAction }) => {
  // Garante compatibilidade com o contrato do AnimalPresenter (foto_url e array de tags).
  const imagemUrl = animal.foto_url || animal.fotoUrl || null;
  const listaTags = Array.isArray(animal.tags)
    ? animal.tags
    : typeof animal.tags === "string" && animal.tags.trim() !== ""
    ? animal.tags.split(",").map((t) => t.trim())
    : [];

  return (
    <article className="bg-white rounded-xl border border-borda overflow-hidden flex flex-col justify-between transition-shadow duration-200 hover:shadow-md">
      <div>
        <div className="aspect-square w-full bg-fundo border-b border-borda flex items-center justify-center overflow-hidden">
          {imagemUrl ? (
            <img
              src={imagemUrl}
              alt={`Foto do animal ${animal.nome}`}
              className="w-full h-full object-cover"
              loading="lazy"
            />
          ) : (
            <span className="text-sm font-medium text-textoApoio px-4 text-center">
              Imagem nao disponivel
            </span>
          )}
        </div>

        {/* Lei da Proximidade: nome e porte pertencem à identificação primária e ficam próximos entre si */}
        <div className="p-5">
          <div className="flex items-baseline justify-between gap-2 mb-3">
            <h2 className="text-xl font-bold text-textoDestaque truncate">
              {animal.nome}
            </h2>
            <span className="text-xs font-semibold uppercase tracking-wider px-2.5 py-1 rounded-full bg-secundaria/20 text-textoDestaque shrink-0">
              {animal.porte}
            </span>
          </div>

          {/* Espaçamento menor (gap-1.5) entre as tags para formar um bloco coeso de características */}
          {listaTags.length > 0 && (
            <div className="flex flex-wrap gap-1.5 mt-3" aria-label="Caracteristicas do animal">
              {listaTags.map((tag, index) => (
                <span
                  key={`${animal.id}-tag-${index}`}
                  className="text-xs bg-fundo text-textoCorpo border border-borda px-2 py-0.5 rounded"
                >
                  {tag}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Affordance: botão de ação primária separado do conteúdo informativo no rodapé do card */}
      <div className="p-5 pt-0 mt-2">
        <Button
          variante="primaria"
          fullWidth
          onClick={() => onClickAction(animal.id)}
        >
          Quero Adotar
        </Button>
      </div>
    </article>
  );
};