# ============================================================
# Makefile - Comandos simplificados para o projeto
# ============================================================

.PHONY: install test test-q1 test-q2 test-q3 run-q1 run-q2 run-q3 lint format clean

# Instalar dependências
install:
	python3 -m venv venv
	source venv/bin/activate && pip install --upgrade pip
	source venv/bin/activate && pip install -r requirements.txt
	source venv/bin/activate && pip install -r requirements-dev.txt

# Executar todos os testes
test:
	source venv/bin/activate && python -m pytest -v

# Testes por questão
test-q1:
	source venv/bin/activate && python -m pytest library_api/tests/ -v

test-q2:
	source venv/bin/activate && python -m pytest tests/test_chatbot.py -v

test-q3:
	source venv/bin/activate && python -m pytest tests/test_semantic_search.py -v

# Executar aplicações
run-q1:
	source venv/bin/activate && uvicorn library_api.main:app --reload --port 8000

run-q2:
	source venv/bin/activate && python -m python_chatbot.main

run-q3:
	source venv/bin/activate && python -m semantic_search.main

# Linting e formatação
lint:
	source venv/bin/activate && flake8 --max-line-length=100 --exclude=venv .
	format:
	source venv/bin/activate && black --exclude=venv .
	source venv/bin/activate && isort --skip=venv .

# Limpar arquivos temporários
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf faiss_index
	rm -rf *.db *.sqlite3
