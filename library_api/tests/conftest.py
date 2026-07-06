"""
Fixtures compartilhadas para os testes da API de biblioteca.

Cria um banco de dados SQLite em memória para cada teste,
garantindo isolamento e reprodutibilidade.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from library_api.main import app
from library_api.database import get_session


@pytest.fixture(name="test_engine")
def test_engine_fixture():
    """
    Cria um engine SQLite em memória para os testes.
    Usa StaticPool para garantir que todas as conexões compartilhem
    o mesmo banco de dados em memória (necessário para SQLite in-memory).
    Cada teste recebe um banco novo e limpo.
    """
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture(name="test_session")
def test_session_fixture(test_engine):
    """
    Fornece uma sessão do banco de dados em memória.
    """
    with Session(test_engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(test_engine):
    """
    Cria um TestClient com o banco de dados em memória.

    Sobrescreve a dependency get_session para usar o engine de teste,
    garantindo que os testes não afetem o banco de dados de produção.
    """

    def get_test_session():
        with Session(test_engine) as session:
            yield session

    # Sobrescreve a dependency no app
    app.dependency_overrides[get_session] = get_test_session

    with TestClient(app) as client:
        yield client

    # Limpa as sobrescritas após o teste
    app.dependency_overrides.clear()
