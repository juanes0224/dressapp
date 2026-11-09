import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.estructuras.heap import MinHeap


def test_heap_vacio_lanza_error_en_pop_y_peek():
    heap: MinHeap[str] = MinHeap()
    assert len(heap) == 0
    with pytest.raises(IndexError):
        heap.pop()
    with pytest.raises(IndexError):
        heap.peek()


def test_pop_devuelve_en_orden_de_prioridad():
    heap: MinHeap[str] = MinHeap()
    heap.push(5.0, "cinco")
    heap.push(1.0, "uno")
    heap.push(3.0, "tres")

    assert heap.peek() == "uno"
    assert [heap.pop(), heap.pop(), heap.pop()] == ["uno", "tres", "cinco"]
    assert len(heap) == 0


def test_desempate_estable_por_orden_de_insercion():
    heap: MinHeap[str] = MinHeap()
    heap.push(1.0, "primero")
    heap.push(1.0, "segundo")
    heap.push(1.0, "tercero")

    assert [heap.pop(), heap.pop(), heap.pop()] == ["primero", "segundo", "tercero"]


def test_heap_con_prioridades_repetidas_no_pierde_elementos():
    heap: MinHeap[int] = MinHeap()
    for valor in [2, 2, 2, 1, 1, 3]:
        heap.push(float(valor), valor)

    salida = [heap.pop() for _ in range(6)]
    assert salida == sorted([2, 2, 2, 1, 1, 3])


@given(
    st.lists(st.floats(min_value=-1e6, max_value=1e6, allow_nan=False), min_size=0, max_size=200)
)
def test_heap_ordena_igual_que_sorted(prioridades: list[float]) -> None:
    """Propiedad: el heap siempre produce el mismo orden que un sorted() estable."""
    heap: MinHeap[int] = MinHeap()
    for indice, prioridad in enumerate(prioridades):
        heap.push(prioridad, indice)

    orden_heap = [heap.pop() for _ in range(len(prioridades))]
    orden_esperado = sorted(range(len(prioridades)), key=lambda i: prioridades[i])

    assert orden_heap == orden_esperado
    assert len(heap) == 0
