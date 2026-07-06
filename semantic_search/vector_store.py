"""
Vector store FAISS para armazenamento e busca de embeddings.

Gerencia a criação, persistência (save/load) e consulta do índice FAISS.
O índice é salvo localmente para evitar regenerar embeddings a cada execução.
"""

from typing import List, Optional

from langchain_community.vectorstores import FAISS

from semantic_search.documents import get_sample_documents
from semantic_search.embeddings import get_embeddings_model

# Diretório onde o índice FAISS é persistido
INDEX_PATH = "faiss_index"


def create_vector_store(documents: Optional[List[dict]] = None) -> FAISS:
    """
    Cria uma vector store FAISS a partir de uma lista de documentos.

    Gera embeddings para cada documento e os armazena no índice FAISS.
    Se nenhum documento for fornecido, usa os documentos de exemplo.

    Args:
        documents: Lista de dicionários com 'id', 'title' e 'content'.
                   Se None, usa get_sample_documents().

    Returns:
        Instância de FAISS com os embeddings indexados.
    """
    if documents is None:
        documents = get_sample_documents()

    # Obtém o modelo de embeddings
    embeddings_model = get_embeddings_model()

    # Prepara os textos e metadados para o FAISS
    texts = [doc["content"] for doc in documents]
    metadatas = [{"id": doc["id"], "title": doc["title"]} for doc in documents]

    # Cria o índice FAISS a partir dos textos e embeddings
    vector_store = FAISS.from_texts(
        texts=texts,
        embedding=embeddings_model,
        metadatas=metadatas,
    )

    return vector_store


def save_vector_store(vector_store: FAISS, path: str = INDEX_PATH) -> None:
    """
    Persiste o índice FAISS em disco para reutilização.

    Args:
        vector_store: Instância de FAISS a ser salva.
        path: Diretório onde o índice será salvo.
    """
    vector_store.save_local(path)


def load_vector_store(path: str = INDEX_PATH) -> Optional[FAISS]:
    """
    Carrega um índice FAISS previamente salvo em disco.

    Args:
        path: Diretório onde o índice está salvo.

    Returns:
        Instância de FAISS carregada, ou None se o índice não existir.
    """
    import os

    if not os.path.exists(path):
        return None

    embeddings_model = get_embeddings_model()
    return FAISS.load_local(
        folder_path=path,
        embeddings=embeddings_model,
        allow_dangerous_deserialization=True,
    )


def get_or_create_vector_store(path: str = INDEX_PATH) -> FAISS:
    """
    Carrega o índice FAISS do disco se existir, ou cria um novo se não existir.

    Esta função evita regenerar embeddings a cada execução, reutilizando
    o índice persistido quando disponível.

    Args:
        path: Diretório do índice FAISS.

    Returns:
        Instância de FAISS pronta para uso.
    """
    # Tenta carregar o índice existente
    vector_store = load_vector_store(path)
    if vector_store is not None:
        return vector_store

    # Cria um novo índice e o persiste
    vector_store = create_vector_store()
    save_vector_store(vector_store, path)
    return vector_store
