# DressApp

Recomendador de outfits según el evento, a partir del closet personal del usuario.

## Qué es

El usuario registra las prendas de su closet (con foto), las clasifica por tipo, color, fit y
nivel de formalidad, y al escoger un evento recibe outfits recomendados. Las recomendaciones se
ajustan con las calificaciones que el usuario da a cada sugerencia.

La decisión de qué outfit recomendar la toma un **motor propio y determinista**: estructuras de
datos implementadas desde cero, puntuación por reglas y aprendizaje por calificaciones. Los
modelos de IA (clasificación de prendas por foto, redacción de explicaciones) son opcionales y
periféricos — nunca deciden qué se recomienda.

## Estado actual

Proyecto en desarrollo activo. Hasta ahora:

- [x] **Etapa 0** — Repositorio, entorno y CI.
- [x] **Etapa 1** — Modelo de dominio y persistencia en SQLite (SQLModel).
- [x] **Etapa 2** — Estructuras de datos propias: trie, min-heap, árbol de categorías y grafo
      dirigido ponderado con Dijkstra.
- [ ] Etapa 3 en adelante — ver [ROADMAP.md](ROADMAP.md).

## Autoría y transparencia

La idea original nació como práctica final de un curso de Estructuras de Datos en equipo (grafo
por capas, Dijkstra, heap, trie, árbol de categorías, tabla hash). Este repositorio es un
**desarrollo individual e independiente** que se extiende más allá del alcance del curso: perfil
de usuario, contexto de clima, API REST completa, aprendizaje por calificaciones, pruebas
automatizadas e integración continua. El historial de Git de este repositorio es la evidencia de
la fecha real de inicio y del avance.

## Stack

Python 3.11+, FastAPI, SQLite + SQLModel, pytest, ruff, mypy. Frontend planeado: React + Vite +
TypeScript (Etapa 9).

## Cómo ejecutar

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac
pip install -e ".[dev]"
cp ../.env.example ../.env    # opcional, valores por defecto ya funcionan
uvicorn app.main:app --reload
```

La API queda disponible en `http://127.0.0.1:8000`, con documentación interactiva en
`http://127.0.0.1:8000/docs`.

## Cómo correr las pruebas

```bash
cd backend
pytest --cov=app --cov-report=term-missing
ruff check .
mypy app
```

## Cargar un closet de ejemplo

```bash
cd backend
python ../scripts/cargar_ejemplo.py
```

Carga ~25 prendas de muestra desde `datos_ejemplo/closet.json` a la base de datos local. El
script es idempotente: correrlo varias veces no duplica datos.

## Documentación

- [`docs/arquitectura.md`](docs/arquitectura.md) — estructura del proyecto y responsabilidades de
  cada módulo.
- [`docs/algoritmos.md`](docs/algoritmos.md) — las estructuras de datos propias, su complejidad y
  el diseño del motor de recomendación.
- [`docs/decisiones/`](docs/decisiones) — ADR (Architecture Decision Records) con cada desviación
  o aclaración sobre la especificación original.
- [`ROADMAP.md`](ROADMAP.md) — plan de trabajo por etapas y qué sigue.

## Decisiones de diseño

El motor de recomendación modela el problema como un **grafo por capas** (superior → exterior
opcional → inferior → calzado → accesorio opcional) y usa **Dijkstra** para encontrar el outfit de
menor costo, porque todos los costos de arista son no negativos. Como el costo de un camino solo
considera pares de prendas consecutivos, el flujo completo usa el algoritmo de **Yen** para
generar varios candidatos y un **re-ranking global** sobre todos los pares de cada outfit — ver
`docs/algoritmos.md` para el detalle y las pruebas de equivalencia con fuerza bruta que lo
verifican.

## Licencia

MIT — ver [LICENSE](LICENSE).
