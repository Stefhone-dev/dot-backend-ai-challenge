"""
Documentos de exemplo para o sistema de busca semântica.

Simula um conjunto de artigos/posts de blog sobre programação em Python.
Estes documentos são usados para gerar embeddings e popular a vector store.
"""

from typing import List, Dict


def get_sample_documents() -> List[Dict[str, str]]:
    """
    Retorna uma lista de documentos de exemplo (posts de blog simulados).

    Cada documento contém:
        - id: Identificador único do documento.
        - title: Título do artigo.
        - content: Conteúdo completo do artigo.

    Returns:
        Lista de dicionários representando os documentos.
    """
    return [
        {
            "id": "doc_01",
            "title": "Introdução ao Python",
            "content": (
                "Python é uma linguagem de programação de alto nível, interpretada "
                "e de propósito geral. Foi criada por Guido van Rossum em 1991. "
                "Python é conhecida por sua sintaxe limpa e legível, que facilita "
                "o aprendizado para iniciantes. É amplamente usada em desenvolvimento "
                "web, automação, análise de dados, inteligência artificial e mais."
            ),
        },
        {
            "id": "doc_02",
            "title": "Listas em Python",
            "content": (
                "Listas são estruturas de dados mutáveis em Python que armazenam "
                "múltiplos valores em uma única variável. Você pode criar uma lista "
                "usando colchetes: minha_lista = [1, 2, 3]. Listas suportam operações "
                "como append, remove, sort e slicing. São ideais para armazenar "
                "coleções ordenadas de itens que podem mudar durante a execução."
            ),
        },
        {
            "id": "doc_03",
            "title": "Dicionários em Python",
            "content": (
                "Dicionários são estruturas de dados que armazenam pares chave-valor. "
                "Em Python, você cria um dicionário com chaves: meu_dict = {'nome': 'João', 'idade': 30}. "
                "Dicionários são mutáveis e permitem acesso rápido aos valores através das chaves. "
                "São amplamente usados para representar objetos JSON e configurações."
            ),
        },
        {
            "id": "doc_04",
            "title": "Compreensão de Listas (List Comprehension)",
            "content": (
                "List comprehension é uma forma concisa e elegante de criar listas em Python. "
                "A sintaxe é: [expressão for item in iterável if condição]. "
                "Exemplo: quadrados = [x**2 for x in range(10)]. "
                "List comprehensions são mais rápidas que loops tradicionais e tornam o código mais legível."
            ),
        },
        {
            "id": "doc_05",
            "title": "Funções e Lambdas em Python",
            "content": (
                "Funções em Python são definidas com a palavra-chave def. "
                "Exemplo: def saudacao(nome): return f'Olá, {nome}!'. "
                "Python também suporta funções anônimas (lambda) para operações simples: "
                "dobro = lambda x: x * 2. Funções podem ter argumentos padrão, "
                "*args e **kwargs para flexibilidade na passagem de parâmetros."
            ),
        },
        {
            "id": "doc_06",
            "title": "Tratamento de Exceções em Python",
            "content": (
                "Python usa blocos try-except para tratamento de exceções. "
                "Exemplo: try: resultado = 10 / 0 except ZeroDivisionError as e: print(e). "
                "Você pode usar finally para executar código independente de erros, "
                "e raise para lançar exceções customizadas. O tratamento adequado de "
                "exceções torna o código mais robusto e confiável."
            ),
        },
        {
            "id": "doc_07",
            "title": "Programação Orientada a Objetos em Python",
            "content": (
                "Python suporta programação orientada a objetos (POO) com classes e herança. "
                "Uma classe é definida com class: class Animal: def __init__(self, nome): self.nome = nome. "
                "Herança permite criar classes especializadas: class Cachorro(Animal). "
                "Python suporta herança múltipla, polimorfismo e encapsulamento."
            ),
        },
        {
            "id": "doc_08",
            "title": "Manipulação de Arquivos em Python",
            "content": (
                "Python oferece funções nativas para manipulação de arquivos. "
                "Para ler um arquivo: with open('arquivo.txt', 'r') as f: conteudo = f.read(). "
                "O bloco with garante o fechamento automático do arquivo. "
                "Você também pode escrever com mode 'w' e adicionar com mode 'a'. "
                "Para arquivos CSV, use o módulo csv; para JSON, use o módulo json."
            ),
        },
    ]
