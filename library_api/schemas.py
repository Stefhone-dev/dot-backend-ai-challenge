"""
Schemas Pydantic para validação de entrada e saída da API.

Separa os schemas de criação (entrada) dos schemas de leitura (saída),
garantindo que o ID nunca seja informado pelo cliente na criação.
"""

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    """
    Schema para criação de um livro (payload de entrada).
    O ID é gerado automaticamente pelo banco de dados.
    """

    title: str = Field(..., min_length=1, max_length=300, description="Título do livro")
    author: str = Field(..., min_length=1, max_length=200, description="Autor do livro")
    publication_date: date = Field(..., description="Data de publicação (formato: YYYY-MM-DD)")
    summary: str = Field(..., min_length=1, max_length=2000, description="Resumo do livro")


class BookRead(BaseModel):
    """
    Schema para leitura de um livro (payload de saída).
    Inclui o ID gerado pelo banco de dados.
    """

    id: int
    title: str
    author: str
    publication_date: date
    summary: str


class BookSearchResult(BaseModel):
    """
    Schema para resultado de busca de livros.
    Inclui o total de resultados encontrados e a lista de livros.
    """

    total: int
    books: list[BookRead]
