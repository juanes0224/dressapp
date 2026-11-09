"""Tabla de prendas del closet."""

from datetime import UTC, datetime

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel

from app.modelos.enums import Categoria, Fit, OrigenClasificacion


class Prenda(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    categoria: Categoria
    subtipo: str
    color_principal: str = Field(description="Color en formato hexadecimal, ej. #1a2b3c")
    color_nombre: str
    fit: Fit
    formalidad: int = Field(ge=1, le=5)
    abrigo: int = Field(ge=1, le=5)
    eventos_aptos: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    imagen_ruta: str | None = Field(default=None)
    origen_clasificacion: OrigenClasificacion = Field(default=OrigenClasificacion.MANUAL)
    creada_en: datetime = Field(default_factory=lambda: datetime.now(UTC))
