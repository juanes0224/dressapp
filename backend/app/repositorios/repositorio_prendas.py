"""Funciones CRUD puras sobre Prenda, separadas de los routers de la API (Etapa 6)."""

from sqlmodel import Session, select

from app.esquemas.prenda import PrendaActualizar, PrendaCrear
from app.modelos.enums import Categoria, Evento, Fit
from app.modelos.prenda import Prenda


def crear_prenda(sesion: Session, datos: PrendaCrear) -> Prenda:
    prenda = Prenda(**datos.model_dump())
    sesion.add(prenda)
    sesion.commit()
    sesion.refresh(prenda)
    return prenda


def obtener_prenda(sesion: Session, prenda_id: int) -> Prenda | None:
    return sesion.get(Prenda, prenda_id)


def listar_prendas(
    sesion: Session,
    categoria: Categoria | None = None,
    color_nombre: str | None = None,
    fit: Fit | None = None,
    evento: Evento | None = None,
) -> list[Prenda]:
    consulta = select(Prenda)
    if categoria is not None:
        consulta = consulta.where(Prenda.categoria == categoria)
    if color_nombre is not None:
        consulta = consulta.where(Prenda.color_nombre == color_nombre)
    if fit is not None:
        consulta = consulta.where(Prenda.fit == fit)

    prendas = list(sesion.exec(consulta).all())
    if evento is not None:
        # eventos_aptos es una columna JSON; se filtra en Python tras la consulta.
        prendas = [p for p in prendas if evento.value in p.eventos_aptos]
    return prendas


def actualizar_prenda(sesion: Session, prenda_id: int, datos: PrendaActualizar) -> Prenda | None:
    prenda = sesion.get(Prenda, prenda_id)
    if prenda is None:
        return None

    cambios = datos.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(prenda, campo, valor)

    sesion.add(prenda)
    sesion.commit()
    sesion.refresh(prenda)
    return prenda


def eliminar_prenda(sesion: Session, prenda_id: int) -> bool:
    prenda = sesion.get(Prenda, prenda_id)
    if prenda is None:
        return False
    sesion.delete(prenda)
    sesion.commit()
    return True
