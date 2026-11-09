# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).

## [Sin publicar]

### Añadido

- Etapa 0: estructura inicial del repositorio, configuración de herramientas (ruff, mypy,
  pytest), endpoint de salud, CI en GitHub Actions, README, roadmap y licencia.
- Etapa 1: modelos de dominio (Prenda, Perfil, Outfit, Calificación, PesoAprendido) persistidos en
  SQLite con SQLModel, repositorios CRUD con validación, closet de ejemplo y script de carga.
- Etapa 2: estructuras de datos propias — trie, min-heap, árbol de categorías y grafo dirigido
  ponderado con Dijkstra — con pruebas unitarias y de propiedad (hypothesis).
