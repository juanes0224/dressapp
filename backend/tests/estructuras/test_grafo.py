import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from app.estructuras.grafo import Grafo


def test_dijkstra_nodo_origen_igual_a_destino():
    grafo = Grafo()
    grafo.agregar_nodo("a")

    assert grafo.dijkstra("a", "a") == (0.0, ["a"])


def test_dijkstra_sin_camino_devuelve_none():
    grafo = Grafo()
    grafo.agregar_nodo("a")
    grafo.agregar_nodo("b")  # sin arista entre ellos

    assert grafo.dijkstra("a", "b") is None


def test_dijkstra_nodo_desconocido_lanza_error():
    grafo = Grafo()
    grafo.agregar_nodo("a")

    with pytest.raises(ValueError):
        grafo.dijkstra("a", "fantasma")
    with pytest.raises(ValueError):
        grafo.dijkstra("fantasma", "a")


def test_agregar_arista_con_peso_negativo_lanza_error():
    grafo = Grafo()
    with pytest.raises(ValueError):
        grafo.agregar_arista("a", "b", -1.0)


def test_dijkstra_elige_el_camino_mas_barato_entre_varios():
    grafo = Grafo()
    grafo.agregar_arista("a", "b", 1.0)
    grafo.agregar_arista("b", "d", 1.0)
    grafo.agregar_arista("a", "c", 0.5)
    grafo.agregar_arista("c", "d", 0.5)

    costo, camino = grafo.dijkstra("a", "d")

    assert costo == pytest.approx(1.0)
    assert camino == ["a", "c", "d"]


def test_dijkstra_con_empate_devuelve_un_camino_valido_de_costo_minimo():
    grafo = Grafo()
    grafo.agregar_arista("a", "b", 1.0)
    grafo.agregar_arista("b", "d", 1.0)
    grafo.agregar_arista("a", "c", 1.0)
    grafo.agregar_arista("c", "d", 1.0)

    costo, camino = grafo.dijkstra("a", "d")

    assert costo == pytest.approx(2.0)
    assert camino in (["a", "b", "d"], ["a", "c", "d"])


def test_vecinos_y_nodos():
    grafo = Grafo()
    grafo.agregar_arista("a", "b", 2.0)
    grafo.agregar_arista("a", "c", 3.0)

    assert set(grafo.nodos()) == {"a", "b", "c"}
    assert grafo.vecinos("a") == [("b", 2.0), ("c", 3.0)]
    assert grafo.vecinos("b") == []


# --- Propiedad: Dijkstra coincide con fuerza bruta en grafos aleatorios pequenos -----------


def _fuerza_bruta(
    adyacencia: dict[int, list[tuple[int, float]]], origen: int, destino: int
) -> float | None:
    """Explora todos los caminos simples (sin repetir nodo) de origen a destino.

    Con pesos >= 0, el optimo siempre es un camino simple: repetir un nodo solo puede
    sumar costo adicional no negativo.
    """
    mejor: float | None = None

    def _dfs(actual: int, visitados: set[int], costo_acumulado: float) -> None:
        nonlocal mejor
        if actual == destino:
            if mejor is None or costo_acumulado < mejor:
                mejor = costo_acumulado
            return
        for vecino, peso in adyacencia.get(actual, []):
            if vecino in visitados:
                continue
            _dfs(vecino, visitados | {vecino}, costo_acumulado + peso)

    _dfs(origen, {origen}, 0.0)
    return mejor


@given(
    n=st.integers(min_value=2, max_value=6),
    semilla_aristas=st.data(),
)
@settings(max_examples=60)
def test_dijkstra_equivale_a_fuerza_bruta_en_grafos_pequenos(
    n: int, semilla_aristas: st.DataObject
) -> None:
    nodos = list(range(n))
    adyacencia: dict[int, list[tuple[int, float]]] = {nodo: [] for nodo in nodos}

    grafo = Grafo()
    for nodo in nodos:
        grafo.agregar_nodo(str(nodo))

    posibles_aristas = [(i, j) for i in nodos for j in nodos if i != j]
    aristas_elegidas = semilla_aristas.draw(
        st.lists(st.sampled_from(posibles_aristas), max_size=len(posibles_aristas), unique=True)
    )

    for origen, destino in aristas_elegidas:
        peso = semilla_aristas.draw(st.floats(min_value=0.0, max_value=5.0, allow_nan=False))
        adyacencia[origen].append((destino, peso))
        grafo.agregar_arista(str(origen), str(destino), peso)

    origen, destino = 0, n - 1

    esperado = _fuerza_bruta(adyacencia, origen, destino)
    resultado = grafo.dijkstra(str(origen), str(destino))

    if esperado is None:
        assert resultado is None
    else:
        assert resultado is not None
        costo_obtenido, _ = resultado
        assert costo_obtenido == pytest.approx(esperado, abs=1e-9)
