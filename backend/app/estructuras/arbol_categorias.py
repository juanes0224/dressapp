"""Arbol de categorias: jerarquia categoria -> subtipo, para validar prendas y filtrar por rama.

Reemplaza el diccionario temporal usado en la Etapa 1 (app.modelos.enums.CATEGORIAS_SUBTIPOS),
que se mantiene como fuente de datos por defecto.
"""

from collections.abc import Mapping

from app.modelos.enums import CATEGORIAS_SUBTIPOS, Categoria


class _NodoCategoria:
    __slots__ = ("nombre", "hijos")

    def __init__(self, nombre: str) -> None:
        self.nombre = nombre
        self.hijos: dict[str, _NodoCategoria] = {}


class ArbolCategorias:
    """Arbol de 3 niveles: raiz -> categoria -> subtipo.

    Complejidad, con P = profundidad del arbol (constante, = 2):
    - es_subtipo_de / categoria_de: O(1) promedio (mapa invertido subtipo -> categoria)
    - subtipos: O(1) (la categoria es hija directa de la raiz)
    - recorrido_dfs: O(n), n = numero total de categorias + subtipos
    """

    def __init__(self, categorias_subtipos: Mapping[Categoria, list[str]] | None = None) -> None:
        datos = categorias_subtipos if categorias_subtipos is not None else CATEGORIAS_SUBTIPOS
        self._raiz = _NodoCategoria("raiz")
        self._categoria_de_subtipo: dict[str, str] = {}

        for categoria, subtipos in datos.items():
            nombre_categoria = categoria.value
            nodo_categoria = _NodoCategoria(nombre_categoria)
            self._raiz.hijos[nombre_categoria] = nodo_categoria
            for subtipo in subtipos:
                nodo_categoria.hijos[subtipo] = _NodoCategoria(subtipo)
                self._categoria_de_subtipo[subtipo] = nombre_categoria

    def es_subtipo_de(self, subtipo: str, categoria: Categoria | str) -> bool:
        nombre_categoria = categoria.value if isinstance(categoria, Categoria) else categoria
        return self._categoria_de_subtipo.get(subtipo) == nombre_categoria

    def categoria_de(self, subtipo: str) -> str | None:
        return self._categoria_de_subtipo.get(subtipo)

    def subtipos(self, categoria: Categoria | str) -> list[str]:
        nombre_categoria = categoria.value if isinstance(categoria, Categoria) else categoria
        nodo = self._raiz.hijos.get(nombre_categoria)
        if nodo is None:
            return []
        return sorted(nodo.hijos)

    def recorrido_dfs(self) -> list[str]:
        """Rutas "categoria" y "categoria/subtipo" en orden alfabetico."""
        resultado: list[str] = []

        def _visitar(nodo: _NodoCategoria, prefijo: str) -> None:
            for nombre in sorted(nodo.hijos):
                hijo = nodo.hijos[nombre]
                ruta = f"{prefijo}/{nombre}" if prefijo else nombre
                resultado.append(ruta)
                _visitar(hijo, ruta)

        _visitar(self._raiz, "")
        return resultado
