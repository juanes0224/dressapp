from collections.abc import Generator

import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

import app.modelos  # noqa: F401  (registra las tablas en SQLModel.metadata)


@pytest.fixture()
def sesion() -> Generator[Session, None, None]:
    motor = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(motor)
    with Session(motor) as sesion:
        yield sesion
