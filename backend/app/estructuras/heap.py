"""Min-heap binario generico, implementado desde cero sobre una lista (sin heapq).

Se usa como cola de prioridad en Dijkstra y en el algoritmo de Yen (Etapa 4).
"""

from typing import Generic, TypeVar

T = TypeVar("T")


class MinHeap(Generic[T]):
    """Heap binario indexado por prioridad (float, menor primero).

    El desempate entre prioridades iguales es estable: se respeta el orden de insercion,
    gracias a un contador interno que rompe los empates antes de comparar el valor (lo que
    tambien evita errores de comparacion entre valores que no son comparables entre si).

    Complejidad: push O(log n), pop O(log n), peek O(1), len O(1).
    """

    def __init__(self) -> None:
        self._datos: list[tuple[float, int, T]] = []
        self._contador = 0

    def __len__(self) -> int:
        return len(self._datos)

    def push(self, prioridad: float, valor: T) -> None:
        entrada = (prioridad, self._contador, valor)
        self._contador += 1
        self._datos.append(entrada)
        self._sift_up(len(self._datos) - 1)

    def pop(self) -> T:
        if not self._datos:
            raise IndexError("pop en heap vacio")
        self._swap(0, len(self._datos) - 1)
        _, _, valor = self._datos.pop()
        if self._datos:
            self._sift_down(0)
        return valor

    def peek(self) -> T:
        if not self._datos:
            raise IndexError("peek en heap vacio")
        return self._datos[0][2]

    def _sift_up(self, indice: int) -> None:
        while indice > 0:
            padre = (indice - 1) // 2
            if self._datos[indice] < self._datos[padre]:
                self._swap(indice, padre)
                indice = padre
            else:
                break

    def _sift_down(self, indice: int) -> None:
        n = len(self._datos)
        while True:
            izquierdo, derecho = 2 * indice + 1, 2 * indice + 2
            menor = indice
            if izquierdo < n and self._datos[izquierdo] < self._datos[menor]:
                menor = izquierdo
            if derecho < n and self._datos[derecho] < self._datos[menor]:
                menor = derecho
            if menor == indice:
                break
            self._swap(indice, menor)
            indice = menor

    def _swap(self, i: int, j: int) -> None:
        self._datos[i], self._datos[j] = self._datos[j], self._datos[i]
