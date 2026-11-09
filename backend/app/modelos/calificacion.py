"""Tabla de calificaciones que el usuario da a un outfit recomendado."""

from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


class Calificacion(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    outfit_id: int = Field(foreign_key="outfit.id")
    valor: int = Field(ge=1, le=5)
    comentario: str | None = Field(default=None)
    creada_en: datetime = Field(default_factory=lambda: datetime.now(UTC))
