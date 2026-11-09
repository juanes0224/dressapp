"""Funciones CRUD puras sobre Perfil. La v1 asume un unico usuario local: siempre hay a lo
sumo una fila, y guardar_perfil hace upsert sobre ella."""

from sqlmodel import Session, select

from app.esquemas.perfil import PerfilEscribir
from app.modelos.perfil import Perfil


def obtener_perfil(sesion: Session) -> Perfil | None:
    return sesion.exec(select(Perfil)).first()


def guardar_perfil(sesion: Session, datos: PerfilEscribir) -> Perfil:
    perfil = obtener_perfil(sesion)
    cambios = datos.model_dump()

    if perfil is None:
        perfil = Perfil(**cambios)
    else:
        for campo, valor in cambios.items():
            setattr(perfil, campo, valor)

    sesion.add(perfil)
    sesion.commit()
    sesion.refresh(perfil)
    return perfil
