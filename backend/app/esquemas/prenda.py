"""DTO de entrada y salida para prendas: validaciones que no dependen de la base de datos."""

import re
from datetime import datetime

from pydantic import BaseModel, field_validator, model_validator

from app.estructuras.arbol_categorias import ArbolCategorias
from app.modelos.enums import Categoria, Evento, Fit, OrigenClasificacion

_PATRON_HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")
_ARBOL_CATEGORIAS = ArbolCategorias()


class _ValidacionesPrenda(BaseModel):
    nombre: str
    categoria: Categoria
    subtipo: str
    color_principal: str
    color_nombre: str
    fit: Fit
    formalidad: int
    abrigo: int
    eventos_aptos: list[Evento] = []

    @field_validator("color_principal")
    @classmethod
    def _validar_color_hex(cls, valor: str) -> str:
        if not _PATRON_HEX.match(valor):
            raise ValueError(
                f"color_principal debe ser hex de 6 digitos, ej. #1a2b3c (recibido: {valor!r})"
            )
        return valor.lower()

    @field_validator("formalidad", "abrigo")
    @classmethod
    def _validar_rango_1_5(cls, valor: int) -> int:
        if not 1 <= valor <= 5:
            raise ValueError(f"debe estar entre 1 y 5 (recibido: {valor})")
        return valor

    @model_validator(mode="after")
    def _validar_subtipo_coherente(self) -> "_ValidacionesPrenda":
        if not _ARBOL_CATEGORIAS.es_subtipo_de(self.subtipo, self.categoria):
            opciones = _ARBOL_CATEGORIAS.subtipos(self.categoria)
            raise ValueError(
                f"subtipo {self.subtipo!r} no pertenece a la categoria {self.categoria.value!r}; "
                f"opciones validas: {opciones}"
            )
        return self


class PrendaCrear(_ValidacionesPrenda):
    imagen_ruta: str | None = None


class PrendaActualizar(BaseModel):
    """Todos los campos son opcionales: solo se actualiza lo que llega."""

    nombre: str | None = None
    categoria: Categoria | None = None
    subtipo: str | None = None
    color_principal: str | None = None
    color_nombre: str | None = None
    fit: Fit | None = None
    formalidad: int | None = None
    abrigo: int | None = None
    eventos_aptos: list[Evento] | None = None
    imagen_ruta: str | None = None

    @field_validator("color_principal")
    @classmethod
    def _validar_color_hex(cls, valor: str | None) -> str | None:
        if valor is not None and not _PATRON_HEX.match(valor):
            raise ValueError(
                f"color_principal debe ser hex de 6 digitos, ej. #1a2b3c (recibido: {valor!r})"
            )
        return valor.lower() if valor else valor

    @field_validator("formalidad", "abrigo")
    @classmethod
    def _validar_rango_1_5(cls, valor: int | None) -> int | None:
        if valor is not None and not 1 <= valor <= 5:
            raise ValueError(f"debe estar entre 1 y 5 (recibido: {valor})")
        return valor


class PrendaLeer(BaseModel):
    id: int
    nombre: str
    categoria: Categoria
    subtipo: str
    color_principal: str
    color_nombre: str
    fit: Fit
    formalidad: int
    abrigo: int
    eventos_aptos: list[str]
    imagen_ruta: str | None
    origen_clasificacion: OrigenClasificacion
    creada_en: datetime

    model_config = {"from_attributes": True}
