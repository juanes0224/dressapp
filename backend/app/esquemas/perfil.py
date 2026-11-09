"""DTO de entrada y salida para el perfil (cuestionario inicial)."""

from pydantic import BaseModel

from app.modelos.enums import Evento, Fit


class PerfilEscribir(BaseModel):
    ciudad: str
    lat: float
    lon: float
    estilos: list[str] = []
    colores_preferidos: list[str] = []
    colores_evitados: list[str] = []
    fit_preferido: Fit
    eventos_frecuentes: list[Evento] = []


class PerfilLeer(PerfilEscribir):
    id: int

    model_config = {"from_attributes": True}
