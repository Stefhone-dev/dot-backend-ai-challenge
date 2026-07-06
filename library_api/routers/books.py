"""
Endpoints da API para gerenciamento de livros.

Define as rotas RESTful para cadastro, consulta, busca e remoção
de livros na biblioteca virtual.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from library_api import crud
from library_api.database import get_session
from library_api.schemas import BookCreate, BookRead, BookSearchResult

router = APIRouter(prefix="/books", tags=["Livros"])


@router.post(
    "/",
    response_model=BookRead,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar um novo livro",
    description=(
        "Cadastra um novo livro na biblioteca virtual. "
        "Os campos obrigatórios são: título, autor, data de publicação e resumo."
    ),
)
def create_book(
    book: BookCreate,
    session: Session = Depends(get_session),
):
    """
    Endpoint para cadastro de livros.

    Recebe os dados do livro via body (JSON) e armazena no banco SQLite.
    Retorna o livro criado com o ID gerado.
    """
    book_data = book.model_dump()
    created_book = crud.create_book(session, book_data)
    return created_book


@router.get(
    "/",
    response_model=list[BookRead],
    summary="Listar todos os livros",
    description=(
        "Retorna a lista de livros cadastrados com paginação. "
        "Use os parâmetros 'skip' e 'limit' para controlar a paginação."
    ),
)
def list_books(
    skip: int = Query(0, ge=0, description="Número de registros a pular (paginação)"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de registros (1-100)"),
    session: Session = Depends(get_session),
):
    """
    Endpoint para listar todos os livros com paginação.
    """
    return crud.get_books(session, skip=skip, limit=limit)


@router.get(
    "/search",
    response_model=BookSearchResult,
    summary="Buscar livros por título ou autor",
    description=(
        "Busca livros por título e/ou autor (busca parcial, case-insensitive). "
        "Se ambos os parâmetros forem fornecidos, retorna livros que "
        "correspondam a qualquer um dos critérios (OR)."
    ),
)
def search_books(
    title: Optional[str] = Query(None, description="Parte do título a buscar"),
    author: Optional[str] = Query(None, description="Parte do nome do autor a buscar"),
    session: Session = Depends(get_session),
):
    """
    Endpoint para busca de livros por título ou autor.

    Realiza busca parcial (LIKE) e case-insensitive.
    Retorna o total de resultados e a lista de livros encontrados.
    """
    if not title and not author:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Forneça pelo menos um parâmetro de busca: 'title' ou 'author'.",
        )

    books = crud.search_books(session, title=title, author=author)
    book_list = [BookRead(**b.model_dump()) for b in books]
    return BookSearchResult(total=len(book_list), books=book_list)


@router.get(
    "/{book_id}",
    response_model=BookRead,
    summary="Consultar um livro por ID",
    description="Retorna os dados de um livro específico pelo seu ID.",
)
def get_book(
    book_id: int,
    session: Session = Depends(get_session),
):
    """
    Endpoint para consultar um livro específico pelo ID.
    Retorna 404 se o livro não for encontrado.
    """
    book = crud.get_book_by_id(session, book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Livro com ID {book_id} não encontrado.",
        )
    return book


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover um livro",
    description="Remove um livro da biblioteca pelo seu ID.",
)
def delete_book(
    book_id: int,
    session: Session = Depends(get_session),
):
    """
    Endpoint para remover um livro pelo ID.
    Retorna 404 se o livro não for encontrado.
    """
    deleted = crud.delete_book(session, book_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Livro com ID {book_id} não encontrado.",
        )
    return None
