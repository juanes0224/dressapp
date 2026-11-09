"""Carga el closet de ejemplo (datos_ejemplo/closet.json) a la base de datos local.

Uso:
    cd backend && python ../scripts/cargar_ejemplo.py

Es idempotente: una prenda ya cargada (mismo nombre) no se vuelve a insertar.
"""

import json
import sys
from pathlib import Path

RAIZ_REPO = Path(__file__).resolve().parent.parent
RUTA_CLOSET_EJEMPLO = RAIZ_REPO / "datos_ejemplo" / "closet.json"


def main() -> None:
    from sqlmodel import Session, select

    from app.db import crear_tablas, motor
    from app.esquemas.prenda import PrendaCrear
    from app.modelos.prenda import Prenda

    crear_tablas()

    with open(RUTA_CLOSET_EJEMPLO, encoding="utf-8") as archivo:
        prendas_crudas = json.load(archivo)

    creadas = 0
    omitidas = 0

    with Session(motor) as sesion:
        for cruda in prendas_crudas:
            ya_existe = sesion.exec(select(Prenda).where(Prenda.nombre == cruda["nombre"])).first()
            if ya_existe is not None:
                omitidas += 1
                continue

            datos = PrendaCrear.model_validate(cruda)
            prenda = Prenda(**datos.model_dump())
            sesion.add(prenda)
            creadas += 1

        sesion.commit()

    print(f"Closet de ejemplo: {creadas} prendas creadas, {omitidas} ya existian.")


if __name__ == "__main__":
    sys.path.insert(0, str(RAIZ_REPO / "backend"))
    main()
