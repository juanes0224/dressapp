"""Motor de base de datos SQLite y sesion para inyeccion de dependencias en FastAPI."""

from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

from app.config import configuracion

argumentos_conexion = {"check_same_thread": False}
motor = create_engine(configuracion.url_base_datos, connect_args=argumentos_conexion)


def crear_tablas() -> None:
    SQLModel.metadata.create_all(motor)


def get_session() -> Generator[Session, None, None]:
    with Session(motor) as sesion:
        yield sesion
