"""Grafo dirigido ponderado (lista de adyacencia) con Dijkstra, implementado desde cero.

Es la base del recomendador (Etapa 4): el grafo por capas usa estos nodos y aristas, y
Dijkstra encuentra el outfit de menor costo.
"""

from app.estructuras.heap import MinHeap


class Grafo:
    """Grafo dirigido ponderado con pesos no negativos (requisito de Dijkstra).

    Complejidad: agregar_nodo O(1), agregar_arista O(1), vecinos O(grado del nodo),
    dijkstra O((V + E) log V) usando el MinHeap propio.
    """

    def __init__(self) -> None:
        self._adyacencia: dict[str, list[tuple[str, float]]] = {}

    def agregar_nodo(self, nodo: str) -> None:
        self._adyacencia.setdefault(nodo, [])

    def agregar_arista(self, origen: str, destino: str, peso: float) -> None:
        if peso < 0:
            raise ValueError(
                f"el peso de una arista debe ser >= 0 para Dijkstra (recibido: {peso})"
            )
        self.agregar_nodo(origen)
        self.agregar_nodo(destino)
        self._adyacencia[origen].append((destino, peso))

    def vecinos(self, nodo: str) -> list[tuple[str, float]]:
        return list(self._adyacencia.get(nodo, []))

    def nodos(self) -> list[str]:
        return list(self._adyacencia)

    def dijkstra(self, origen: str, destino: str) -> tuple[float, list[str]] | None:
        """Costo y camino de menor costo de `origen` a `destino`.

        Devuelve None si no hay camino. Lanza ValueError si `origen` o `destino` no
        pertenecen al grafo. Valido porque todos los pesos son >= 0 (se garantiza en
        agregar_arista): el primer pop de cada nodo ya trae su distancia definitiva.
        """
        if origen not in self._adyacencia:
            raise ValueError(f"nodo origen desconocido: {origen!r}")
        if destino not in self._adyacencia:
            raise ValueError(f"nodo destino desconocido: {destino!r}")

        distancias: dict[str, float] = {origen: 0.0}
        predecesores: dict[str, str] = {}
        visitados: set[str] = set()

        cola: MinHeap[str] = MinHeap()
        cola.push(0.0, origen)

        while len(cola) > 0:
            actual = cola.pop()
            if actual in visitados:
                continue
            visitados.add(actual)

            if actual == destino:
                break

            for vecino, peso in self._adyacencia[actual]:
                nueva_distancia = distancias[actual] + peso
                if vecino not in distancias or nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    predecesores[vecino] = actual
                    cola.push(nueva_distancia, vecino)

        if destino not in distancias:
            return None

        camino = [destino]
        while camino[-1] != origen:
            camino.append(predecesores[camino[-1]])
        camino.reverse()

        return distancias[destino], camino
