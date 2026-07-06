"""
Camada de operações CRUD (Create, Read, Update, Delete) para livros.

Centraliza toda a lógica de acesso ao banco de dados,
mantendo os routers limpos e focados em HTTP.
"""

from datetime import date
from typing import Optional

from sqlmodel import Session, or_, select

from library_api.models import Book


def create_book(session: Session, book_data: dict) -> Book:
    """
    Cria um novo livro no banco de dados.

    Args:
        session: Sessão ativa do banco de dados.
        book_data: Dicionário com os campos do livro.

    Returns:
        A instância de Book criada (com ID preenchido).
    """
    book = Book(**book_data)
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


def get_book_by_id(session: Session, book_id: int) -> Optional[Book]:
    """
    Busca um livro pelo seu ID.

    Args:
        session: Sessão ativa do banco de dados.
        book_id: ID do livro a ser buscado.

    Returns:
        A instância de Book ou None se não encontrado.
    """
    statement = select(Book).where(Book.id == book_id)
    return session.exec(statement).first()


def get_books(
    session: Session,
    skip: int = 0,
    limit: int = 10,
) -> list[Book]:
    """
    Lista todos os livros com paginação.

    Args:
        session: Sessão ativa do banco de dados.
        skip: Número de registros a pular (offset para paginação).
        limit: Número máximo de registros a retornar.

    Returns:
        Lista de instâncias de Book.
    """
    statement = select(Book).offset(skip).limit(limit)
    return list(session.exec(statement).all())


def search_books(
    session: Session,
    title: Optional[str] = None,
    author: Optional[str] = None,
) -> list[Book]:
    """
    Busca livros por título e/ou autor (busca parcial, case-insensitive).

    Se ambos title e author forem fornecidos, retorna livros que
    correspondam a qualquer um dos critérios (OR).

    Args:
        session: Sessão ativa do banco de dados.
        title: Parte do título a buscar (opcional).
        author: Parte do nome do autor a buscar (opcional).

    Returns:
        Lista de instâncias de Book que correspondem aos critérios.
    """
    conditions = []
    if title:
        # ilike faz busca case-insensitive no SQLite
        conditions.append(Book.title.ilike(f"%{title}%"))
    if author:
        conditions.append(Book.author.ilike(f"%{author}%"))

    if not conditions:
        return []

    statement = select(Book).where(or_(*conditions))
    return list(session.exec(statement).all())


def delete_book(session: Session, book_id: int) -> bool:
    """
    Remove um livro do banco de dados pelo ID.

    Args:
        session: Sessão ativa do banco de dados.
        book_id: ID do livro a ser removido.

    Returns:
        True se o livro foi removido, False se não foi encontrado.
    """
    book = get_book_by_id(session, book_id)
    if book is None:
        return False
    session.delete(book)
    session.commit()
    return True
