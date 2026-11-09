# Roadmap

Plan de trabajo por etapas. Una etapa a la vez, en orden. Ver el documento de especificación
completo para el detalle de tareas y criterios de aceptación de cada una.

## Completadas

- [x] **Etapa 0 — Repositorio y entorno.** Estructura de carpetas, `pyproject.toml`, CI con lint,
      tipos y pruebas, endpoint `/api/salud`, licencia y documentación base.
- [x] **Etapa 1 — Modelo de dominio y persistencia.** Tablas SQLModel para Prenda, Perfil, Outfit,
      Calificación y PesoAprendido. Repositorios CRUD, validaciones y datos de ejemplo.
- [x] **Etapa 2 — Estructuras de datos propias.** Trie, min-heap, árbol de categorías y grafo
      dirigido ponderado con Dijkstra, implementados desde cero y con pruebas de propiedad.

## En curso / siguientes

- [ ] **Etapa 3 — Motor de puntuación.** Compatibilidad de color (rueda HSL), idoneidad de una
      prenda para un evento `u(p,e)`, compatibilidad entre prendas `c(p,q)` y puntaje global de un
      outfit `G(outfit)`, como funciones puras con desglose explicable.
- [ ] **Etapa 4 — Recomendador.** Construcción del grafo por capas, mejor outfit con Dijkstra,
      top-K con el algoritmo de Yen, re-ranking global con diversidad y backtracking con poda para
      completar un outfit alrededor de una prenda fija.
- [ ] **Etapa 5 — Perfil inicial y aprendizaje.** Cuestionario de perfil editable y actualización
      de los pesos aprendidos a partir de las calificaciones del usuario.
- [ ] **Etapa 6 — API REST.** Routers completos, subida de imágenes con validación y miniaturas,
      formato uniforme de errores, documentación OpenAPI.
- [ ] **Etapa 7 — Contexto de clima.** Cliente de Open-Meteo con caché y degradación elegante.
- [ ] **Etapa 8 — Clasificación por foto (tentativa).** Evaluación de `open_clip` para sugerir tipo
      y color desde la imagen; se adopta solo si el acierto y el tiempo por imagen lo justifican.
- [ ] **Etapa 9 — Frontend web.** React + Vite + TypeScript: closet, alta de prenda,
      recomendaciones, calificación y favoritos.
- [ ] **Etapa 10 — Explicaciones de los outfits.** Explicador por plantilla a partir del desglose
      del motor, con un LLM opcional como redactor (nunca como quien decide).
- [ ] **Etapa 11 — Calidad, documentación y entrega v1.0.** Cobertura, Docker Compose, README
      final, changelog y release v1.0.0.

## Más allá de v1.0

- Autenticación y múltiples usuarios (v1 asume un único usuario local).
- App móvil.
- Calendario de uso y control de repetición de prendas.
- Compartir outfits y recomendación de compras.
- Fine-tuning del modelo de visión sobre closets reales.
- Métricas de calidad de recomendación (precisión percibida vía calificaciones agregadas).
