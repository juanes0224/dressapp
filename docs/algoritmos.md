# Algoritmos y estructuras de datos

Las estructuras de esta sección están implementadas desde cero en
[`backend/app/estructuras/`](../backend/app/estructuras), sin librerías externas. Cada una tiene
pruebas unitarias y, cuando aplica, una prueba de propiedad con `hypothesis` en
[`backend/tests/estructuras/`](../backend/tests/estructuras).

## Trie

**Archivo:** [`trie.py`](../backend/app/estructuras/trie.py)

Árbol de prefijos indexado por carácter, usado para el autocompletado y la búsqueda de prendas
por nombre (`GET /api/prendas/buscar?q=`, Etapa 6). Cada nodo terminal guarda un **conjunto de
ids**, porque varias prendas distintas pueden compartir el mismo nombre (ej. dos "camiseta
blanca"). Las palabras se normalizan (minúsculas, sin tildes) antes de insertarse o buscarse, con
`unicodedata`, para que la búsqueda sea insensible a mayúsculas y acentos.

| Operación        | Complejidad    |
| ----------------- | -------------- |
| `insertar`         | O(L)           |
| `eliminar`          | O(L)           |
| `buscar_prefijo`    | O(L + k)       |

L = longitud de la palabra normalizada, k = número de resultados devueltos.

`eliminar` poda hacia atrás los nodos que quedan sin ids ni hijos, para no dejar memoria muerta
cuando se borra una prenda.

## MinHeap

**Archivo:** [`heap.py`](../backend/app/estructuras/heap.py)

Heap binario genérico sobre una lista, sin usar `heapq`. Es la cola de prioridad de Dijkstra y
del algoritmo de Yen (Etapa 4). Cada entrada es `(prioridad, contador, valor)`: el contador de
inserción rompe los empates de forma estable (FIFO entre prioridades iguales) y evita además
comparar `valor` directamente, lo que permitiría que el heap reciba valores no comparables entre
sí (p. ej. tuplas heterogéneas).

| Operación | Complejidad |
| --------- | ----------- |
| `push`    | O(log n)    |
| `pop`     | O(log n)    |
| `peek`    | O(1)        |
| `len`     | O(1)        |

**Prueba de propiedad** (`test_heap_ordena_igual_que_sorted`): para cualquier lista de
prioridades, la secuencia de `pop()` coincide exactamente con `sorted(..., key=prioridad)`, que en
Python es un sort estable — la misma garantía de desempate del heap.

## Árbol de categorías

**Archivo:** [`arbol_categorias.py`](../backend/app/estructuras/arbol_categorias.py)

Árbol de tres niveles (raíz → categoría → subtipo) construido a partir del catálogo fijo
`CATEGORIAS_SUBTIPOS` (`app/modelos/enums.py`). Reemplaza el diccionario temporal que se usaba en
la Etapa 1 para validar que el `subtipo` de una prenda sea coherente con su `categoria`
(`app/esquemas/prenda.py`).

| Operación        | Complejidad |
| ----------------- | ----------- |
| `es_subtipo_de`     | O(1) promedio (mapa invertido subtipo → categoría) |
| `categoria_de`      | O(1) promedio |
| `subtipos`          | O(1) (la categoría es hija directa de la raíz) |
| `recorrido_dfs`     | O(n), n = categorías + subtipos |

## Grafo dirigido ponderado y Dijkstra

**Archivo:** [`grafo.py`](../backend/app/estructuras/grafo.py)

Grafo dirigido con lista de adyacencia. `agregar_arista` rechaza pesos negativos con
`ValueError` apenas se intentan insertar, porque **Dijkstra solo es correcto cuando todos los
pesos son ≥ 0**: en ese caso, la primera vez que un nodo sale del heap, su distancia ya es
definitiva (no puede mejorarse después por ningún otro camino, porque cualquier arista adicional
solo puede sumar costo, nunca restarlo).

`dijkstra(origen, destino)` usa el `MinHeap` propio y la técnica de **borrado perezoso**: en vez
de un `decrease-key` (que el heap no soporta), cada mejora de distancia simplemente empuja una
nueva entrada; al sacar un nodo ya visitado, se descarta. Devuelve `(costo, camino)` o `None` si
no hay camino.

| Caso                     | Complejidad          |
| ------------------------- | -------------------- |
| `agregar_nodo/arista`       | O(1)                  |
| `dijkstra`                  | O((V + E) log V)      |

Esta es exactamente la pieza central del recomendador (Etapa 4): el grafo por capas
(superior → exterior opcional → inferior → calzado → accesorio opcional) usa estas aristas para
que Dijkstra encuentre el outfit de menor costo. Ver `docs/arquitectura.md` y la sección 2.5 del
plan de trabajo para el diseño completo con Yen y el re-ranking global.

**Prueba de propiedad** (`test_dijkstra_equivale_a_fuerza_bruta_en_grafos_pequenos`): sobre
grafos aleatorios de 2 a 6 nodos y pesos en `[0, 5]`, el costo que devuelve `dijkstra` coincide
con el mínimo obtenido por **fuerza bruta**, enumerando todos los caminos simples con DFS. Con
pesos no negativos, el óptimo siempre es un camino simple (repetir un nodo solo puede sumar costo
adicional), así que la comparación es válida.

## Qué sigue

La Etapa 3 construye el motor de puntuación (`u(p,e)`, `c(p,q)`, `G(outfit)`) sobre estas
estructuras, y la Etapa 4 ensambla el recomendador completo: grafo por capas + Dijkstra para el
mejor outfit, Yen para los top-K candidatos, re-ranking global por diversidad y backtracking con
poda para completar un outfit alrededor de una prenda fija. Ver [`ROADMAP.md`](../ROADMAP.md).
