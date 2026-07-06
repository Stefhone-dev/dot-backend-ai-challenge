"""
Aplicação FastAPI — API de Biblioteca Virtual.

Ponto de entrada da API. Configura a aplicação, inicializa o banco
de dados e registra os routers.

Execução:
    uvicorn library_api.main:app --reload --port 8000

Documentação interativa:
    Swagger UI:  http://localhost:8000/docs
    ReDoc:       http://localhost:8000/redoc
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from library_api.database import init_db
from library_api.routers import books


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação.
    Inicializa o banco de dados na inicialização (cria tabelas se necessário).
    """
    init_db()
    yield


# Cria a aplicação FastAPI com metadados descritivos
app = FastAPI(
    title="Biblioteca Virtual API",
    description=(
        "API para cadastro e consulta de livros em uma biblioteca virtual. "
        "Construída com FastAPI, SQLModel e SQLite."
    ),
    version="1.0.0",
    contact={
        "name": "Desafio Backend IA — Grupo DOT",
    },
    lifespan=lifespan,
)


@app.get("/", tags=["Health"])
def root():
    """
    Endpoint raiz — verificação de saúde da API.
    """
    return {"status": "ok", "message": "Biblioteca Virtual API está ativa."}


@app.get("/health", tags=["Health"])
def health_check():
    """
    Endpoint de health check para monitoramento.
    """
    return {"status": "healthy"}


# Registra o router de livros
app.include_router(books.router)
