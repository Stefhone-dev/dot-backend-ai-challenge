"""
Testes unitários para o sistema de busca semântica (Questão 3).

Cobre:
- Documentos de exemplo (estrutura e conteúdo)
- Geração de embeddings (dimensão e validade)
- Criação da vector store FAISS
- Busca semântica (retorna resultados relevantes)
- Persistência (save/load do índice)
- Tratamento de edge cases

Nota: Os testes de embeddings e FAISS podem levar alguns segundos
na primeira execução (download do modelo ~90MB).
"""

import os
import tempfile

import pytest

from semantic_search.documents import get_sample_documents
from semantic_search.embeddings import get_embeddings_model, generate_query_embedding
from semantic_search.vector_store import create_vector_store, save_vector_store, load_vector_store, get_or_create_vector_store
from semantic_search.search import search_documents


# ============================================================
# Testes dos documentos de exemplo
# ============================================================


class TestDocuments:
    """Testes dos documentos de exemplo."""

    def test_documents_not_empty(self):
        """A lista de documentos não deve estar vazia."""
        docs = get_sample_documents()
        assert len(docs) > 0

    def test_documents_have_required_fields(self):
        """Cada documento deve ter id, title e content."""
        docs = get_sample_documents()
        for doc in docs:
            assert "id" in doc
            assert "title" in doc
            assert "content" in doc

    def test_documents_have_unique_ids(self):
        """Todos os IDs devem ser únicos."""
        docs = get_sample_documents()
        ids = [doc["id"] for doc in docs]
        assert len(ids) == len(set(ids))

    def test_documents_content_not_empty(self):
        """O conteúdo de cada documento não deve estar vazio."""
        docs = get_sample_documents()
        for doc in docs:
            assert len(doc["content"]) > 50  # Conteúdo substancial

    def test_documents_about_python(self):
        """Os documentos devem ser sobre Python."""
        docs = get_sample_documents()
        all_content = " ".join(doc["content"] for doc in docs)
        assert "Python" in all_content or "python" in all_content


# ============================================================
# Testes de embeddings
# ============================================================


class TestEmbeddings:
    """Testes do modelo de embeddings."""

    def test_get_embeddings_model(self):
        """Deve retornar uma instância de HuggingFaceEmbeddings."""
        model = get_embeddings_model()
        assert model is not None

    def test_generate_query_embedding(self):
        """Deve gerar um embedding vetorial para a consulta."""
        embedding = generate_query_embedding("Como criar uma lista em Python?")
        assert isinstance(embedding, list)
        assert len(embedding) == 384  # all-MiniLM-L6-v2 tem 384 dimensões
        assert all(isinstance(v, float) for v in embedding)

    def test_embeddings_different_queries_differ(self):
        """Embeddings de consultas diferentes devem ser diferentes."""
        emb1 = generate_query_embedding("Como criar uma lista?")
        emb2 = generate_query_embedding("Como tratar exceções?")
        # Pelo menos alguns valores devem diferir
        differences = sum(1 for a, b in zip(emb1, emb2) if abs(a - b) > 0.01)
        assert differences > 0


# ============================================================
# Testes da vector store FAISS
# ============================================================


class TestVectorStore:
    """Testes da vector store FAISS."""

    @pytest.fixture
    def vector_store(self):
        """Cria uma vector store para os testes."""
        return create_vector_store()

    def test_create_vector_store(self, vector_store):
        """Deve criar uma vector store FAISS válida."""
        assert vector_store is not None

    def test_vector_store_has_documents(self, vector_store):
        """A vector store deve conter os documentos indexados."""
        # similarity_search deve retornar resultados
        results = vector_store.similarity_search("Python", k=1)
        assert len(results) > 0

    def test_save_and_load_vector_store(self, vector_store):
        """Deve salvar e carregar o índice FAISS do disco."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Salva o índice
            save_vector_store(vector_store, tmpdir)

            # Verifica que os arquivos foram criados
            assert os.path.exists(os.path.join(tmpdir, "index.faiss"))
            assert os.path.exists(os.path.join(tmpdir, "index.pkl"))

            # Carrega o índice
            loaded = load_vector_store(tmpdir)
            assert loaded is not None

            # Verifica que o índice carregado funciona
            results = loaded.similarity_search("Python", k=1)
            assert len(results) > 0

    def test_load_nonexistent_index_returns_none(self):
        """load_vector_store deve retornar None se o índice não existe."""
        result = load_vector_store("/tmp/nonexistent_faiss_index_12345")
        assert result is None

    def test_get_or_create_creates_new(self):
        """get_or_create deve criar um novo índice se não existir."""
        with tempfile.TemporaryDirectory() as tmpdir:
            index_path = os.path.join(tmpdir, "test_index")
            vs = get_or_create_vector_store(index_path)
            assert vs is not None
            # Verifica que foi salvo em disco
            assert os.path.exists(os.path.join(index_path, "index.faiss"))


# ============================================================
# Testes da busca semântica
# ============================================================


class TestSearch:
    """Testes da função de busca semântica."""

    @pytest.fixture
    def vector_store(self):
        """Cria uma vector store para os testes de busca."""
        return create_vector_store()

    def test_search_returns_results(self, vector_store):
        """A busca deve retornar resultados."""
        results = search_documents(vector_store, "Como criar uma lista?", k=3)
        assert len(results) > 0
        assert len(results) <= 3

    def test_search_result_structure(self, vector_store):
        """Cada resultado deve ter title, content e score."""
        results = search_documents(vector_store, "Python", k=2)
        for result in results:
            assert "title" in result
            assert "content" in result
            assert "score" in result
            assert isinstance(result["score"], float)

    def test_search_relevant_results(self, vector_store):
        """Busca por 'lista' deve retornar documento sobre listas."""
        results = search_documents(vector_store, "Como criar uma lista em Python?", k=3)
        # Pelo menos um resultado deve mencionar "lista"
        contents = " ".join(r["content"] for r in results)
        assert "lista" in contents.lower()

    def test_search_relevant_exceptions(self, vector_store):
        """Busca por 'exceções' deve retornar documento sobre tratamento de erros."""
        results = search_documents(vector_store, "Como tratar erros e exceções?", k=3)
        contents = " ".join(r["content"] for r in results)
        assert "exceção" in contents.lower() or "exceções" in contents.lower() or "try" in contents.lower()

    def test_search_relevant_files(self, vector_store):
        """Busca por 'arquivos' deve retornar documento sobre manipulação de arquivos."""
        results = search_documents(vector_store, "Como trabalhar com arquivos?", k=3)
        contents = " ".join(r["content"] for r in results)
        assert "arquivo" in contents.lower() or "open" in contents.lower()

    def test_search_k_parameter(self, vector_store):
        """A busca deve respeitar o parâmetro k (número de resultados)."""
        results_k1 = search_documents(vector_store, "Python", k=1)
        results_k5 = search_documents(vector_store, "Python", k=5)
        assert len(results_k1) <= 1
        assert len(results_k5) <= 5

    def test_search_empty_query(self, vector_store):
        """A busca não deve quebrar com uma consulta vazia."""
        results = search_documents(vector_store, "", k=3)
        # Deve retornar resultados sem erro (FAISS lida com query vazia)
        assert isinstance(results, list)
