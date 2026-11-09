"""Configuracion de la aplicacion, cargada desde variables de entorno (.env)."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuracion(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Base de datos
    url_base_datos: str = "sqlite:///./dressapp.db"

    # Carga de imagenes
    directorio_subidas: str = "uploads"
    tamano_maximo_imagen_mb: int = 5

    # Clasificador de imagenes por IA (Etapa 8, desactivado por defecto)
    clasificador_activo: bool = False

    # Explicador con LLM (Etapa 10, desactivado por defecto)
    clave_api_llm: str | None = None

    # Clima (Etapa 7)
    clima_timeout_segundos: float = 3.0
    clima_cache_minutos: int = 30

    # CORS para el frontend local
    origenes_permitidos: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]


configuracion = Configuracion()
