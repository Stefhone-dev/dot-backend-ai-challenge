# dot-backend-ai-challenge

Desafio técnico para Desenvolvedor Backend com foco em IA — Grupo DOT.

Este projeto implementa as três questões do desafio em uma estrutura de monorepo
organizada e profissional, utilizando Python, FastAPI, Langchain e FAISS.

---

## Estrutura do Projeto

```
dot-backend-ai-challenge/
├── .github/workflows/ci.yml      # CI: lint + testes automáticos
├── .env.example                   # Template de variáveis de ambiente
├── .gitignore
├── Makefile                       # Comandos simplificados
├── README.md
├── requirements.txt               # Dependências principais
├── requirements-dev.txt           # Dependências de desenvolvimento
│
├── library_api/                   # Questão 1: API de Biblioteca Virtual
│   ├── main.py                    # App FastAPI + documentação OpenAPI
│   ├── database.py                # Engine SQLite + session
│   ├── models.py                  # SQLModel: Book
│   ├── schemas.py                 # Pydantic: BookCreate, BookRead, BookSearchResult
│   ├── crud.py                    # Operações CRUD + busca
│   ├── routers/books.py           # Endpoints RESTful
│   └── tests/                     # 26 testes unitários
│
├── python_chatbot/                # Questão 2: Chatbot com IA Generativa
│   ├── main.py                    # Chatbot terminal interativo
│   ├── chain.py                   # LCEL chain + memória (ChatbotChain)
│   ├── llm_provider.py            # Provider-agnostic (OpenAI/Groq)
│   └── prompts.py                 # System prompt especializado em Python
│
├── semantic_search/               # Questão 3: Busca Semântica
│   ├── main.py                    # Demonstração executável no terminal
│   ├── documents.py               # 8 documentos de exemplo sobre Python
│   ├── embeddings.py              # Geração de embeddings (sentence-transformers)
│   ├── vector_store.py            # FAISS: criar, salvar, carregar índice
│   └── search.py                  # Função de busca semântica
│
├── shared/                        # Config compartilhada
│   └── config.py                  # Settings via pydantic-settings
│
└── tests/                         # Testes integrados
    ├── test_chatbot.py            # 23 testes (FakeLLM, sem API key)
    └── test_semantic_search.py    # 20 testes (FAISS + embeddings)
```

---

## Pré-requisitos

- Python 3.9+
- pip

---

## Instalação

```bash
# 1. Clonar o repositório
git clone https://github.com/Stefhone-dev/dot-backend-ai-challenge.git
cd dot-backend-ai-challenge

# 2. Criar ambiente virtual e instalar dependências
make install

# 3. Configurar variáveis de ambiente (apenas para Questão 2)
cp .env.example .env
# Edite o .env com sua API key
```

---

## Questão 1: API de Biblioteca Virtual

API RESTful construída com **FastAPI** + **SQLModel** + **SQLite**.

### Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/` | Health check raiz |
| `GET` | `/health` | Status da API |
| `POST` | `/books/` | Cadastrar um novo livro |
| `GET` | `/books/` | Listar livros (com paginação `skip`, `limit`) |
| `GET` | `/books/search` | Buscar livros por `title` e/ou `author` |
| `GET` | `/books/{book_id}` | Consultar livro por ID |
| `DELETE` | `/books/{book_id}` | Remover livro por ID |

### Executar a API

```bash
make run-q1
```

Acesse a documentação interativa:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Executar os testes

```bash
make test-q1
```

---

## Questão 2: Chatbot com IA Generativa

Chatbot usando **Langchain** com **LangChain Expression Language (LCEL)**,
memória de conversação e modelo GPT-4 da OpenAI.

### Configuração

O chatbot suporta dois provedores de LLM:

1. **OpenAI (padrão)** — GPT-4, conforme exigido pelo desafio
2. **Groq (alternativa gratuita)** — Llama 3 70B, para testes locais

Configure no arquivo `.env`:

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sua-chave-aqui
```

### Executar o chatbot

```bash
make run-q2
```

### Executar os testes

Os testes usam `FakeListChatModel` (mock) e rodam **sem nenhuma API key**:

```bash
make test-q2
```

---

## Questão 3: Busca Semântica com Vector Stores e Embeddings

Sistema de busca semântica usando **sentence-transformers** (all-MiniLM-L6-v2)
e **FAISS** como vector store.

### Como funciona

1. 8 documentos de exemplo sobre Python são carregados
2. Embeddings de 384 dimensões são gerados para cada documento
3. Os embeddings são armazenados em um índice FAISS local
4. A busca compara o embedding da consulta com os embeddings armazenados

### Executar a demonstração

```bash
make run-q3
```

Na primeira execução, o modelo de embeddings (~90MB) é baixado automaticamente.
Nas execuções seguintes, o índice FAISS é carregado do disco (persistência).

### Executar os testes

```bash
make test-q3
```

---

## Executar Todos os Testes

```bash
make test
```

Resultado: **69 testes passando** (26 Q1 + 23 Q2 + 20 Q3).

---

## Tecnologias Utilizadas

| Tecnologia | Versão | Uso |
|---|---|---|
| Python | 3.9+ | Linguagem principal |
| FastAPI | 0.128.8 | Framework de API (Q1) |
| SQLModel | 0.0.34 | ORM + validação (Q1) |
| SQLite | — | Banco de dados (Q1) |
| Langchain | 0.3.30 | Framework de IA (Q2) |
| Langchain-OpenAI | 0.3.35 | Integração com GPT-4 (Q2) |
| FAISS | 1.13.0 | Vector store (Q3) |
| sentence-transformers | 5.1.2 | Embeddings locais (Q3) |
| pytest | 8.4.2 | Testes unitários |
| pydantic-settings | 2.11.0 | Gestão de configuração |

---

## Arquitetura

### Clean Code e Boas Práticas

- **Modularização**: Cada questão é um módulo independente
- **Separação de responsabilidades**: CRUD, routers, schemas e models separados
- **Tratamento de exceções**: Erros 404, 422 e 400 tratados explicitamente
- **Código comentado**: Toda função e classe documentada com docstrings
- **PEP 8**: Código segue padrões Python
- **Type hints**: Tipagem estática em todo o código
- **Provider-agnostic**: Q2 funciona com qualquer LLM via Langchain

### Testes

- **69 testes unitários** cobrindo happy path, edge cases e erros
- **Sem dependências externas**: Q1 e Q3 rodam 100% offline
- **Mock de LLM**: Q2 usa FakeListChatModel (sem API key)
- **Banco em memória**: Q1 usa SQLite in-memory nos testes
