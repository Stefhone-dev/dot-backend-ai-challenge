"""
Geração de embeddings usando sentence-transformers.

Utiliza o modelo all-MiniLM-L6-v2 da HuggingFace, que é leve, rápido
e não requer API key (roda localmente). Gera embeddings vetoriais
de 384 dimensões para cada documento.
"""

from typing import List

from langchain_community.embeddings import HuggingFaceEmbeddings

# Nome do modelo de embeddings (leve e eficiente)
# all-MiniLM-L6-v2: 384 dimensões, ~90MB, otimizado para busca semântica
MODEL_NAME = "all-MiniLM-L6-v2"


def get_embeddings_model() -> HuggingFaceEmbeddings:
    """
    Cria e retorna o modelo de embeddings.

    O modelo all-MiniLM-L6-v2 é baixado automaticamente na primeira execução
    (aproximadamente 90MB) e fica em cache para execuções subsequentes.

    Returns:
        Instância de HuggingFaceEmbeddings configurada.
    """
    return HuggingFaceEmbeddings(
        model_name=MODEL_NAME,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Gera embeddings para uma lista de textos.

    Args:
        texts: Lista de textos para gerar embeddings.

    Returns:
        Lista de vetores de embeddings (cada vetor tem 384 dimensões).
    """
    model = get_embeddings_model()
    return model.embed_documents(texts)


def generate_query_embedding(query: str) -> List[float]:
    """
    Gera embedding para um texto de consulta (query).

    Args:
        query: Texto de busca.

    Returns:
        Vetor de embedding da consulta (384 dimensões).
    """
    model = get_embeddings_model()
    return model.embed_query(query)
