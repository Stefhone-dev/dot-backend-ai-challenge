"""
Testes unitários para os endpoints da API de biblioteca.

Cobre:
- Criação de livros (happy path + validação)
- Listagem com paginação
- Busca por título e autor
- Consulta por ID (incluindo 404)
- Remoção (incluindo 404)
- Edge cases e tratamento de erros
"""

from datetime import date

from fastapi.testclient import TestClient


# ============================================================
# Dados de teste reutilizáveis
# ============================================================

VALID_BOOK = {
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "publication_date": "2008-08-01",
    "summary": "Um guia para escrever código limpo, legível e maintível.",
}

SECOND_BOOK = {
    "title": "Fluent Python",
    "author": "Luciano Ramalho",
    "publication_date": "2015-08-20",
    "summary": "Livro detalhado sobre as melhores práticas em Python.",
}

THIRD_BOOK = {
    "title": "Python Crash Course",
    "author": "Eric Matthes",
    "publication_date": "2019-05-03",
    "summary": "Introdução prática à programação em Python.",
}


# ============================================================
# Testes do endpoint raiz e health check
# ============================================================


class TestHealthEndpoints:
    """Testes dos endpoints de verificação de saúde."""

    def test_root(self, client: TestClient):
        """Endpoint raiz deve retornar status ok."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    def test_health_check(self, client: TestClient):
        """Endpoint /health deve retornar status healthy."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


# ============================================================
# Testes do endpoint POST /books/ (criação)
# ============================================================


class TestCreateBook:
    """Testes do endpoint de cadastro de livros."""

    def test_create_book_success(self, client: TestClient):
        """Deve criar um livro com dados válidos e retornar 201."""
        response = client.post("/books/", json=VALID_BOOK)
        assert response.status_code == 201

        data = response.json()
        assert data["id"] is not None
        assert data["title"] == "Clean Code"
        assert data["author"] == "Robert C. Martin"
        assert data["publication_date"] == "2008-08-01"
        assert data["summary"] == VALID_BOOK["summary"]

    def test_create_book_missing_title(self, client: TestClient):
        """Deve retornar 422 quando o título está ausente."""
        invalid_book = VALID_BOOK.copy()
        del invalid_book["title"]
        response = client.post("/books/", json=invalid_book)
        assert response.status_code == 422

    def test_create_book_missing_author(self, client: TestClient):
        """Deve retornar 422 quando o autor está ausente."""
        invalid_book = VALID_BOOK.copy()
        del invalid_book["author"]
        response = client.post("/books/", json=invalid_book)
        assert response.status_code == 422

    def test_create_book_missing_publication_date(self, client: TestClient):
        """Deve retornar 422 quando a data de publicação está ausente."""
        invalid_book = VALID_BOOK.copy()
        del invalid_book["publication_date"]
        response = client.post("/books/", json=invalid_book)
        assert response.status_code == 422

    def test_create_book_missing_summary(self, client: TestClient):
        """Deve retornar 422 quando o resumo está ausente."""
        invalid_book = VALID_BOOK.copy()
        del invalid_book["summary"]
        response = client.post("/books/", json=invalid_book)
        assert response.status_code == 422

    def test_create_book_empty_title(self, client: TestClient):
        """Deve retornar 422 quando o título é uma string vazia."""
        invalid_book = VALID_BOOK.copy()
        invalid_book["title"] = ""
        response = client.post("/books/", json=invalid_book)
        assert response.status_code == 422

    def test_create_book_empty_author(self, client: TestClient):
        """Deve retornar 422 quando o autor é uma string vazia."""
        invalid_book = VALID_BOOK.copy()
        invalid_book["author"] = ""
        response = client.post("/books/", json=invalid_book)
        assert response.status_code == 422

    def test_create_book_invalid_date_format(self, client: TestClient):
        """Deve retornar 422 quando a data está em formato inválido."""
        invalid_book = VALID_BOOK.copy()
        invalid_book["publication_date"] = "01-08-2008"
        response = client.post("/books/", json=invalid_book)
        assert response.status_code == 422

    def test_create_book_title_too_long(self, client: TestClient):
        """Deve retornar 422 quando o título excede 300 caracteres."""
        invalid_book = VALID_BOOK.copy()
        invalid_book["title"] = "A" * 301
        response = client.post("/books/", json=invalid_book)
        assert response.status_code == 422


# ============================================================
# Testes do endpoint GET /books/ (listagem)
# ============================================================


class TestListBooks:
    """Testes do endpoint de listagem de livros."""

    def test_list_empty(self, client: TestClient):
        """Deve retornar lista vazia quando não há livros cadastrados."""
        response = client.get("/books/")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_with_books(self, client: TestClient):
        """Deve retornar todos os livros cadastrados."""
        client.post("/books/", json=VALID_BOOK)
        client.post("/books/", json=SECOND_BOOK)

        response = client.get("/books/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_list_pagination(self, client: TestClient):
        """Deve respeitar os parâmetros de paginação skip e limit."""
        # Cria 3 livros
        client.post("/books/", json=VALID_BOOK)
        client.post("/books/", json=SECOND_BOOK)
        client.post("/books/", json=THIRD_BOOK)

        # Página 1: limit=2
        response = client.get("/books/?skip=0&limit=2")
        assert response.status_code == 200
        assert len(response.json()) == 2

        # Página 2: skip=2, limit=2
        response = client.get("/books/?skip=2&limit=2")
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_list_invalid_skip(self, client: TestClient):
        """Deve retornar 422 quando skip é negativo."""
        response = client.get("/books/?skip=-1")
        assert response.status_code == 422

    def test_list_invalid_limit(self, client: TestClient):
        """Deve retornar 422 quando limit é maior que 100."""
        response = client.get("/books/?limit=101")
        assert response.status_code == 422


# ============================================================
# Testes do endpoint GET /books/search (busca)
# ============================================================


class TestSearchBooks:
    """Testes do endpoint de busca de livros."""

    def test_search_by_title(self, client: TestClient):
        """Deve encontrar livros pelo título (busca parcial)."""
        client.post("/books/", json=VALID_BOOK)
        client.post("/books/", json=SECOND_BOOK)

        response = client.get("/books/search?title=Clean")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert "Clean" in data["books"][0]["title"]

    def test_search_by_author(self, client: TestClient):
        """Deve encontrar livros pelo autor (busca parcial)."""
        client.post("/books/", json=VALID_BOOK)
        client.post("/books/", json=SECOND_BOOK)

        response = client.get("/books/search?author=Ramalho")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert "Ramalho" in data["books"][0]["author"]

    def test_search_by_title_and_author(self, client: TestClient):
        """Deve retornar livros que correspondam a título OU autor."""
        client.post("/books/", json=VALID_BOOK)
        client.post("/books/", json=SECOND_BOOK)
        client.post("/books/", json=THIRD_BOOK)

        # Busca "Python" no título e "Martin" no autor (OR)
        # Clean Code → autor "Martin" ✓
        # Fluent Python → título "Python" ✓
        # Python Crash Course → título "Python" ✓
        response = client.get("/books/search?title=Python&author=Martin")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3

    def test_search_case_insensitive(self, client: TestClient):
        """Deve realizar busca case-insensitive."""
        client.post("/books/", json=VALID_BOOK)

        response = client.get("/books/search?title=clean")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1

    def test_search_no_results(self, client: TestClient):
        """Deve retornar total 0 quando não há correspondências."""
        client.post("/books/", json=VALID_BOOK)

        response = client.get("/books/search?title=NonExistentBook")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["books"] == []

    def test_search_no_params(self, client: TestClient):
        """Deve retornar 400 quando nenhum parâmetro de busca é fornecido."""
        response = client.get("/books/search")
        assert response.status_code == 400


# ============================================================
# Testes do endpoint GET /books/{book_id} (consulta por ID)
# ============================================================


class TestGetBook:
    """Testes do endpoint de consulta de livro por ID."""

    def test_get_book_success(self, client: TestClient):
        """Deve retornar os dados do livro quando o ID existe."""
        create_response = client.post("/books/", json=VALID_BOOK)
        book_id = create_response.json()["id"]

        response = client.get(f"/books/{book_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == book_id
        assert data["title"] == "Clean Code"

    def test_get_book_not_found(self, client: TestClient):
        """Deve retornar 404 quando o ID não existe."""
        response = client.get("/books/999")
        assert response.status_code == 404
        assert "não encontrado" in response.json()["detail"]


# ============================================================
# Testes do endpoint DELETE /books/{book_id} (remoção)
# ============================================================


class TestDeleteBook:
    """Testes do endpoint de remoção de livro."""

    def test_delete_book_success(self, client: TestClient):
        """Deve remover o livro e retornar 204."""
        create_response = client.post("/books/", json=VALID_BOOK)
        book_id = create_response.json()["id"]

        response = client.delete(f"/books/{book_id}")
        assert response.status_code == 204

        # Verifica que o livro não existe mais
        get_response = client.get(f"/books/{book_id}")
        assert get_response.status_code == 404

    def test_delete_book_not_found(self, client: TestClient):
        """Deve retornar 404 ao tentar remover um ID inexistente."""
        response = client.delete("/books/999")
        assert response.status_code == 404
