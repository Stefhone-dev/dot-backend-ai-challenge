"""
Modelo de dados da biblioteca virtual.

Define o modelo Book usando SQLModel, que combina ORM (SQLAlchemy)
com validação de tipos (Pydantic) em uma única classe.
"""

from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel


class Book(SQLModel, table=True):
    """
    Modelo de um livro na biblioteca virtual.

    Atributos:
        id: Identificador único (chave primária, auto-incremento).
        title: Título do livro (obrigatório).
        author: Autor do livro (obrigatório).
        publication_date: Data de publicação (obrigatório).
        summary: Resumo do livro (obrigatório).
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, min_length=1, max_length=300)
    author: str = Field(index=True, min_length=1, max_length=200)
    publication_date: date = Field(description="Data de publicação do livro")
    summary: str = Field(min_length=1, max_length=2000)
