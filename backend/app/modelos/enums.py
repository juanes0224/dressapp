"""Catalogos fijos del dominio: categorias, fit, eventos y origen de clasificacion."""

from enum import StrEnum


class Categoria(StrEnum):
    SUPERIOR = "superior"
    EXTERIOR = "exterior"
    INFERIOR = "inferior"
    CALZADO = "calzado"
    ACCESORIO = "accesorio"


class Fit(StrEnum):
    """El valor numerico asociado es el volumen de la prenda (ver FIT_A_VOLUMEN)."""

    SLIM = "slim"
    REGULAR = "regular"
    BAGGY = "baggy"
    ULTRA_BAGGY = "ultra_baggy"


FIT_A_VOLUMEN: dict[Fit, int] = {
    Fit.SLIM: 1,
    Fit.REGULAR: 2,
    Fit.BAGGY: 3,
    Fit.ULTRA_BAGGY: 4,
}


class Evento(StrEnum):
    """Catalogo fijo de eventos. El valor numerico es la formalidad objetivo (ver
    EVENTO_A_FORMALIDAD)."""

    MUY_FORMAL = "muy_formal"
    MEDIO_FORMAL = "medio_formal"
    CASUAL = "casual"
    NOCTURNO = "nocturno"
    DISCOTECA = "discoteca"


EVENTO_A_FORMALIDAD: dict[Evento, int] = {
    Evento.MUY_FORMAL: 5,
    Evento.MEDIO_FORMAL: 4,
    Evento.CASUAL: 2,
    Evento.NOCTURNO: 3,
    Evento.DISCOTECA: 3,
}


class OrigenClasificacion(StrEnum):
    MANUAL = "manual"
    IA = "ia"


# Diccionario temporal categoria -> subtipos validos.
# TODO(Etapa 2): reemplazar por app.estructuras.arbol_categorias.ArbolCategorias,
# que ofrece la misma validacion mas busqueda por rama y recorrido DFS.
CATEGORIAS_SUBTIPOS: dict[Categoria, list[str]] = {
    Categoria.SUPERIOR: ["camiseta", "camisa", "polo", "buzo", "blusa"],
    Categoria.EXTERIOR: ["chaqueta", "blazer", "abrigo", "chaleco"],
    Categoria.INFERIOR: ["jean", "pantalon", "sudadera", "short", "falda"],
    Categoria.CALZADO: ["tenis", "zapato_formal", "bota", "sandalia"],
    Categoria.ACCESORIO: ["reloj", "gorra", "cinturon", "collar", "bolso"],
}
