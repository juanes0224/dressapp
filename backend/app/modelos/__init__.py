"""Modelos de dominio (tablas SQLModel). Se importan aqui para que su metadata quede
registrada antes de llamar a app.db.crear_tablas()."""

from app.modelos.calificacion import Calificacion
from app.modelos.enums import (
    CATEGORIAS_SUBTIPOS,
    EVENTO_A_FORMALIDAD,
    FIT_A_VOLUMEN,
    Categoria,
    Evento,
    Fit,
    OrigenClasificacion,
)
from app.modelos.outfit import Outfit
from app.modelos.perfil import Perfil
from app.modelos.peso_aprendido import PesoAprendido
from app.modelos.prenda import Prenda

__all__ = [
    "CATEGORIAS_SUBTIPOS",
    "EVENTO_A_FORMALIDAD",
    "FIT_A_VOLUMEN",
    "Calificacion",
    "Categoria",
    "Evento",
    "Fit",
    "OrigenClasificacion",
    "Outfit",
    "Perfil",
    "PesoAprendido",
    "Prenda",
]
