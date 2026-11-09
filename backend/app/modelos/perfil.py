"""Tabla de perfil del usuario (cuestionario inicial, v1 asume un unico usuario local)."""

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel

from app.modelos.enums import Fit


class Perfil(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    ciudad: str
    lat: float
    lon: float
    estilos: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    colores_preferidos: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    colores_evitados: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    fit_preferido: Fit
    eventos_frecuentes: list[str] = Field(default_factory=list, sa_column=Column(JSON))
