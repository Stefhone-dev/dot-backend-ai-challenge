"""
Demonstração do sistema de busca semântica.

Ponto de entrada da Questão 3. Cria (ou carrega) a vector store FAISS,
executa buscas semânticas de exemplo e imprime os resultados no terminal.

Execução:
    python -m semantic_search.main
"""

from semantic_search.search import search_and_display
from semantic_search.vector_store import get_or_create_vector_store


def run_demo():
    """
    Executa a demonstração da busca semântica.

    1. Carrega ou cria o índice FAISS com os documentos de exemplo.
    2. Executa 3 consultas diferentes para demonstrar o funcionamento.
    3. Imprime os resultados relevantes no terminal.
    """
    print("=" * 60)
    print("  Busca Semântica com FAISS + Embeddings")
    print("=" * 60)
    print()
    print("  Inicializando vector store FAISS...")
    print("  (Na primeira execução, o modelo de embeddings será baixado)")
    print()

    # Carrega ou cria a vector store
    vector_store = get_or_create_vector_store()

    print("  Vector store pronta!")
    print()

    # Consultas de exemplo para demonstração
    demo_queries = [
        "Como criar uma lista em Python?",
        "Como tratar erros e exceções no Python?",
        "Como trabalhar com arquivos em Python?",
    ]

    print("=" * 60)
    print("  Demonstração de Busca Semântica")
    print("=" * 60)

    for query in demo_queries:
        search_and_display(vector_store, query, k=3)

    print("\nDemonstração concluída!")


if __name__ == "__main__":
    run_demo()
