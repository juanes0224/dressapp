"""Punto de entrada de la aplicacion FastAPI."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import configuracion

app = FastAPI(
    title="DressApp",
    description="Recomendador de outfits segun el evento a partir del closet personal.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=configuracion.origenes_permitidos,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/salud")
def salud() -> dict[str, str]:
    """Health check basico: confirma que el servicio esta en linea."""
    return {"estado": "ok"}
