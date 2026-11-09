"""Tabla de outfits recomendados: snapshot para poder calificarlos y marcarlos favoritos."""

from datetime import UTC, datetime

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel

from app.modelos.enums import Evento


class Outfit(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    evento: Evento
    prendas: list[int] = Field(
        default_factory=list,
        sa_column=Column(JSON),
        description="ids de Prenda, ordenadas por capa",
    )
    puntaje: float = Field(ge=0.0, le=1.0)
    explicacion: str = Field(default="")
    favorito: bool = Field(default=False)
    creado_en: datetime = Field(default_factory=lambda: datetime.now(UTC))
