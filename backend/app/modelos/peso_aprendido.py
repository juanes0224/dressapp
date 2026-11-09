"""Tabla de pesos aprendidos por calificacion para cada par de prendas y evento.

La clave logica es (prenda_a, prenda_b, evento) con prenda_a < prenda_b: el par se guarda una
sola vez, sin importar el orden en que las prendas aparecieron en el outfit calificado.
"""

from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlmodel import Field, SQLModel

from app.modelos.enums import Evento


class PesoAprendido(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("prenda_a", "prenda_b", "evento", name="uq_peso_par_evento"),
        CheckConstraint("prenda_a < prenda_b", name="ck_peso_orden_par"),
    )

    id: int | None = Field(default=None, primary_key=True)
    prenda_a: int = Field(foreign_key="prenda.id")
    prenda_b: int = Field(foreign_key="prenda.id")
    evento: Evento
    valor: float = Field(ge=0.0, le=1.0)
    n_calificaciones: int = Field(default=0, ge=0)
