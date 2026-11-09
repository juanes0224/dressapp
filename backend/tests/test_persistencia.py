import pytest
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from app.esquemas.perfil import PerfilEscribir
from app.esquemas.prenda import PrendaActualizar, PrendaCrear
from app.modelos.enums import Categoria, Evento, Fit
from app.modelos.peso_aprendido import PesoAprendido
from app.repositorios import repositorio_perfil, repositorio_prendas


def _datos_camiseta(**sobreescritos: object) -> PrendaCrear:
    base = dict(
        nombre="Camiseta blanca",
        categoria=Categoria.SUPERIOR,
        subtipo="camiseta",
        color_principal="#FFFFFF",
        color_nombre="blanco",
        fit=Fit.SLIM,
        formalidad=1,
        abrigo=1,
        eventos_aptos=[Evento.CASUAL],
    )
    base.update(sobreescritos)
    return PrendaCrear(**base)


# --- Prenda: CRUD ---------------------------------------------------------


def test_crear_y_obtener_prenda(sesion: Session) -> None:
    prenda = repositorio_prendas.crear_prenda(sesion, _datos_camiseta())

    assert prenda.id is not None
    assert prenda.color_principal == "#ffffff"  # normalizado a minusculas
    assert repositorio_prendas.obtener_prenda(sesion, prenda.id) is not None


def test_obtener_prenda_inexistente_devuelve_none(sesion: Session) -> None:
    assert repositorio_prendas.obtener_prenda(sesion, 9999) is None


def test_listar_prendas_con_filtros(sesion: Session) -> None:
    repositorio_prendas.crear_prenda(sesion, _datos_camiseta(nombre="Camiseta casual"))
    repositorio_prendas.crear_prenda(
        sesion,
        _datos_camiseta(
            nombre="Camisa formal",
            subtipo="camisa",
            color_nombre="azul_marino",
            color_principal="#1B2A4A",
            fit=Fit.REGULAR,
            formalidad=4,
            eventos_aptos=[Evento.MUY_FORMAL],
        ),
    )

    todas = repositorio_prendas.listar_prendas(sesion)
    assert len(todas) == 2

    solo_formales = repositorio_prendas.listar_prendas(sesion, evento=Evento.MUY_FORMAL)
    assert [p.nombre for p in solo_formales] == ["Camisa formal"]

    solo_azules = repositorio_prendas.listar_prendas(sesion, color_nombre="azul_marino")
    assert [p.nombre for p in solo_azules] == ["Camisa formal"]


def test_actualizar_prenda(sesion: Session) -> None:
    prenda = repositorio_prendas.crear_prenda(sesion, _datos_camiseta())

    actualizada = repositorio_prendas.actualizar_prenda(
        sesion, prenda.id, PrendaActualizar(nombre="Camiseta renombrada", formalidad=2)
    )

    assert actualizada is not None
    assert actualizada.nombre == "Camiseta renombrada"
    assert actualizada.formalidad == 2
    assert actualizada.color_nombre == "blanco"  # lo que no se envia, no cambia


def test_actualizar_prenda_inexistente_devuelve_none(sesion: Session) -> None:
    assert repositorio_prendas.actualizar_prenda(sesion, 9999, PrendaActualizar(nombre="x")) is None


def test_eliminar_prenda(sesion: Session) -> None:
    prenda = repositorio_prendas.crear_prenda(sesion, _datos_camiseta())

    assert repositorio_prendas.eliminar_prenda(sesion, prenda.id) is True
    assert repositorio_prendas.obtener_prenda(sesion, prenda.id) is None
    assert repositorio_prendas.eliminar_prenda(sesion, prenda.id) is False


# --- Prenda: validacion -----------------------------------------------------


def test_formalidad_fuera_de_rango_es_rechazada() -> None:
    with pytest.raises(ValidationError):
        _datos_camiseta(formalidad=7)


def test_abrigo_fuera_de_rango_es_rechazado() -> None:
    with pytest.raises(ValidationError):
        _datos_camiseta(abrigo=0)


def test_color_no_hexadecimal_es_rechazado() -> None:
    with pytest.raises(ValidationError):
        _datos_camiseta(color_principal="blanco")


def test_subtipo_de_otra_categoria_es_rechazado() -> None:
    with pytest.raises(ValidationError):
        _datos_camiseta(categoria=Categoria.SUPERIOR, subtipo="jean")  # jean es de "inferior"


# --- Perfil -----------------------------------------------------------------


def test_guardar_perfil_crea_y_luego_actualiza(sesion: Session) -> None:
    datos_iniciales = PerfilEscribir(
        ciudad="Medellin",
        lat=6.25,
        lon=-75.56,
        estilos=["casual"],
        colores_preferidos=["azul_marino"],
        colores_evitados=["rosado"],
        fit_preferido=Fit.REGULAR,
        eventos_frecuentes=[Evento.CASUAL],
    )
    primero = repositorio_perfil.guardar_perfil(sesion, datos_iniciales)

    segundo = repositorio_perfil.guardar_perfil(
        sesion,
        PerfilEscribir(
            ciudad="Bogota",
            lat=4.71,
            lon=-74.07,
            fit_preferido=Fit.SLIM,
        ),
    )

    assert primero.id == segundo.id  # mismo registro, no uno nuevo
    assert segundo.ciudad == "Bogota"
    assert repositorio_perfil.obtener_perfil(sesion).ciudad == "Bogota"


# --- PesoAprendido: unicidad (a, b, evento) con a < b ------------------------


def test_peso_aprendido_respeta_unicidad_del_par(sesion: Session) -> None:
    a = repositorio_prendas.crear_prenda(sesion, _datos_camiseta(nombre="A"))
    b = repositorio_prendas.crear_prenda(sesion, _datos_camiseta(nombre="B"))
    ids_ordenados = sorted([a.id, b.id])

    sesion.add(
        PesoAprendido(
            prenda_a=ids_ordenados[0],
            prenda_b=ids_ordenados[1],
            evento=Evento.CASUAL,
            valor=0.5,
            n_calificaciones=1,
        )
    )
    sesion.commit()

    sesion.add(
        PesoAprendido(
            prenda_a=ids_ordenados[0],
            prenda_b=ids_ordenados[1],
            evento=Evento.CASUAL,
            valor=0.9,
            n_calificaciones=2,
        )
    )
    with pytest.raises(IntegrityError):
        sesion.commit()


def test_peso_aprendido_rechaza_par_en_desorden(sesion: Session) -> None:
    a = repositorio_prendas.crear_prenda(sesion, _datos_camiseta(nombre="A"))
    b = repositorio_prendas.crear_prenda(sesion, _datos_camiseta(nombre="B"))
    ids_ordenados = sorted([a.id, b.id])

    sesion.add(
        PesoAprendido(
            prenda_a=ids_ordenados[1],  # invertido a proposito: a > b
            prenda_b=ids_ordenados[0],
            evento=Evento.CASUAL,
            valor=0.5,
            n_calificaciones=1,
        )
    )
    with pytest.raises(IntegrityError):
        sesion.commit()
