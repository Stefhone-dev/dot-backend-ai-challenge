"""
Função de busca semântica.

Implementa a busca que, dado um texto de consulta, retorna os documentos
mais relevantes com base na similaridade semântica (cosseno) entre
o embedding da consulta e os embeddings dos documentos.
"""

from typing import List, Dict

from langchain_community.vectorstores import FAISS


def search_documents(
    vector_store: FAISS,
    query: str,
    k: int = 3,
) -> List[Dict]:
    """
    Busca documentos semanticamente similares à consulta.

    Utiliza similarity_search_with_score do FAISS, que retorna os
    documentos mais próximos junto com o score de similaridade.

    Args:
        vector_store: Instância de FAISS com os embeddings indexados.
        query: Texto de consulta para a busca.
        k: Número máximo de documentos a retornar (top-K).

    Returns:
        Lista de dicionários, cada um contendo:
            - 'title': Título do documento.
            - 'content': Conteúdo do documento.
            - 'score': Score de similaridade (menor = mais similar).
    """
    # Realiza a busca com score de similaridade
    results = vector_store.similarity_search_with_score(query, k=k)

    # Formata os resultados
    formatted_results = []
    for doc, score in results:
        formatted_results.append({
            "title": doc.metadata.get("title", "Sem título"),
            "content": doc.page_content,
            "score": float(score),
        })

    return formatted_results


def search_and_display(
    vector_store: FAISS,
    query: str,
    k: int = 3,
) -> List[Dict]:
    """
    Busca documentos e imprime os resultados formatados no terminal.

    Args:
        vector_store: Instância de FAISS com os embeddings indexados.
        query: Texto de consulta.
        k: Número máximo de documentos a retornar.

    Returns:
        Lista de resultados formatados (mesmo que search_documents).
    """
    results = search_documents(vector_store, query, k=k)

    print(f"\nConsulta: '{query}'")
    print(f"Resultados encontrados: {len(results)}")
    print("-" * 60)

    for i, result in enumerate(results, 1):
        print(f"\n  [{i}] {result['title']}")
        print(f"      Score de similaridade: {result['score']:.4f}")
        # Exibe os primeiros 150 caracteres do conteúdo
        preview = result["content"][:150]
        print(f"      Conteúdo: {preview}...")

    print("\n" + "-" * 60)

    return results
