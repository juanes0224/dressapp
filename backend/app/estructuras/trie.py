"""Trie (arbol de prefijos) para autocompletado y busqueda de prendas por nombre.

Cada nodo final guarda un conjunto de ids, porque varias prendas pueden compartir el mismo
nombre normalizado (ej. dos "camiseta blanca" distintas). Implementado desde cero, sin
dependencias externas.
"""

import unicodedata


def _normalizar(palabra: str) -> str:
    """minusculas y sin tildes/diacriticos, para que la busqueda sea insensible a ambos."""
    sin_tildes = unicodedata.normalize("NFKD", palabra).encode("ascii", "ignore").decode("ascii")
    return sin_tildes.lower().strip()


class _NodoTrie:
    __slots__ = ("hijos", "ids")

    def __init__(self) -> None:
        self.hijos: dict[str, _NodoTrie] = {}
        self.ids: set[int] = set()


class Trie:
    """Trie de minusculas/sin tildes, indexado por caracter.

    Complejidad, con L = longitud de la palabra normalizada y k = resultados devueltos:
    - insertar / eliminar: O(L)
    - buscar_prefijo: O(L + k)
    """

    def __init__(self) -> None:
        self._raiz = _NodoTrie()

    def insertar(self, palabra: str, id_prenda: int) -> None:
        """Inserta `id_prenda` bajo la palabra normalizada. O(L)."""
        nodo = self._raiz
        for letra in _normalizar(palabra):
            nodo = nodo.hijos.setdefault(letra, _NodoTrie())
        nodo.ids.add(id_prenda)

    def eliminar(self, palabra: str, id_prenda: int) -> bool:
        """Quita `id_prenda` de la palabra y poda nodos que quedan vacios. O(L).

        Devuelve True si existia y se elimino; False si la palabra o el id no estaban.
        """
        letras = _normalizar(palabra)
        camino: list[_NodoTrie] = [self._raiz]
        nodo = self._raiz
        for letra in letras:
            siguiente = nodo.hijos.get(letra)
            if siguiente is None:
                return False
            nodo = siguiente
            camino.append(nodo)

        if id_prenda not in nodo.ids:
            return False
        nodo.ids.discard(id_prenda)

        for i in range(len(camino) - 1, 0, -1):
            actual = camino[i]
            if actual.ids or actual.hijos:
                break
            padre = camino[i - 1]
            del padre.hijos[letras[i - 1]]

        return True

    def buscar_prefijo(self, prefijo: str, limite: int = 10) -> list[int]:
        """Ids de prendas cuyo nombre normalizado empieza por `prefijo`, hasta `limite`
        resultados, recorridos en orden alfabetico (DFS). O(L + k)."""
        if limite <= 0:
            return []

        nodo = self._raiz
        for letra in _normalizar(prefijo):
            siguiente = nodo.hijos.get(letra)
            if siguiente is None:
                return []
            nodo = siguiente

        resultados: list[int] = []
        self._recolectar(nodo, resultados, limite)
        return resultados

    def _recolectar(self, nodo: _NodoTrie, resultados: list[int], limite: int) -> None:
        if len(resultados) >= limite:
            return
        for id_prenda in sorted(nodo.ids):
            if len(resultados) >= limite:
                return
            resultados.append(id_prenda)
        for letra in sorted(nodo.hijos):
            if len(resultados) >= limite:
                return
            self._recolectar(nodo.hijos[letra], resultados, limite)
