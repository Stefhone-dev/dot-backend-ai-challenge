"""
Testes unitários para o chatbot (Questão 2).

Utiliza FakeMessagesListChatModel para simular respostas do LLM,
permitindo testar a chain LCEL, prompts e memória sem nenhuma API key.

Cobre:
- Criação da chain LCEL
- System prompt especializado em Python
- Fluxo de pergunta e resposta
- Memória de conversação
- Tratamento de erros (API key ausente)
- Exemplos de perguntas e respostas
"""

import pytest
from langchain_community.chat_models.fake import FakeListChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from python_chatbot.chain import ChatbotChain, create_simple_chain
from python_chatbot.prompts import create_prompt, SYSTEM_PROMPT
from python_chatbot.llm_provider import get_llm


# ============================================================
# Fixtures
# ============================================================

# Resposta genérica que contém palavras-chave relevantes para todos os testes
_FAKE_RESPONSE = (
    "Para trabalhar com listas e tuplas em Python, "
    "você pode usar list comprehension: [x**2 for x in range(10)]. "
    "Listas são mutáveis enquanto tuplas são imutáveis."
)


@pytest.fixture
def fake_llm():
    """
    Cria um FakeListChatModel que simula respostas do LLM.
    Permite testar a chain sem nenhuma API key.
    """
    return FakeListChatModel(responses=[_FAKE_RESPONSE])


@pytest.fixture
def fake_chain(fake_llm):
    """Cria uma chain LCEL simples com o LLM fake para testes."""
    return create_simple_chain(fake_llm)


# ============================================================
# Testes do prompt template
# ============================================================


class TestPrompt:
    """Testes do template de prompt do chatbot."""

    def test_system_prompt_contains_python(self):
        """O system prompt deve mencionar Python."""
        assert "Python" in SYSTEM_PROMPT

    def test_system_prompt_contains_expert(self):
        """O system prompt deve definir o papel de especialista."""
        assert "especialista" in SYSTEM_PROMPT.lower()

    def test_create_prompt_returns_template(self):
        """create_prompt deve retornar um ChatPromptTemplate."""
        prompt = create_prompt()
        assert prompt is not None

    def test_prompt_has_system_message(self):
        """O prompt deve incluir a mensagem de sistema."""
        prompt = create_prompt()
        # Formata o prompt com valores de teste
        formatted = prompt.format_messages(
            input="Teste",
            history=[],
        )
        # A primeira mensagem deve ser o system prompt
        assert isinstance(formatted[0], SystemMessage)
        assert "Python" in formatted[0].content

    def test_prompt_has_human_placeholder(self):
        """O prompt deve incluir o input do usuário."""
        prompt = create_prompt()
        formatted = prompt.format_messages(
            input="Como criar uma lista?",
            history=[],
        )
        # A última mensagem deve ser o input do usuário
        human_msg = formatted[-1]
        assert isinstance(human_msg, HumanMessage)
        assert "Como criar uma lista?" in human_msg.content

    def test_prompt_includes_history(self):
        """O prompt deve incluir o histórico da conversa quando fornecido."""
        prompt = create_prompt()
        history = [
            HumanMessage(content="Pergunta anterior"),
            AIMessage(content="Resposta anterior"),
        ]
        formatted = prompt.format_messages(
            input="Nova pergunta",
            history=history,
        )
        # Deve ter: system + 2 mensagens de histórico + 1 human = 4
        assert len(formatted) == 4


# ============================================================
# Testes da chain LCEL
# ============================================================


class TestChain:
    """Testes da chain LCEL do chatbot."""

    def test_chain_returns_response(self, fake_chain):
        """A chain deve retornar uma resposta de texto."""
        response = fake_chain.invoke({"input": "Como criar uma lista?", "history": []})
        assert isinstance(response, str)
        assert len(response) > 0

    def test_chain_response_about_list(self, fake_chain):
        """A chain deve responder sobre criação de listas."""
        response = fake_chain.invoke({"input": "Como criar uma lista?", "history": []})
        assert "lista" in response.lower()

    def test_chain_response_about_tuple(self, fake_chain):
        """A chain deve responder sobre diferença entre lista e tupla."""
        response = fake_chain.invoke({"input": "Qual a diferença entre lista e tupla?", "history": []})
        assert "tupla" in response.lower()

    def test_chain_response_about_comprehension(self, fake_chain):
        """A chain deve responder sobre list comprehension."""
        response = fake_chain.invoke({"input": "Como usar list comprehension?", "history": []})
        assert "comprehension" in response.lower() or "lista" in response.lower()


# ============================================================
# Testes do provider de LLM
# ============================================================


class TestLLMProvider:
    """Testes do provider-agnostic de LLM."""

    def test_get_llm_openai_without_key_raises_error(self, monkeypatch):
        """Deve lançar ValueError quando OPENAI_API_KEY não está configurada."""
        from shared.config import Settings

        # Cria settings sem API key
        test_settings = Settings(openai_api_key=None, llm_provider="openai")
        monkeypatch.setattr("python_chatbot.llm_provider.settings", test_settings)

        with pytest.raises(ValueError, match="OPENAI_API_KEY"):
            get_llm()

    def test_get_llm_groq_without_key_raises_error(self, monkeypatch):
        """Deve lançar ValueError quando GROQ_API_KEY não está configurada."""
        from shared.config import Settings

        test_settings = Settings(groq_api_key=None, llm_provider="groq")
        monkeypatch.setattr("python_chatbot.llm_provider.settings", test_settings)

        with pytest.raises(ValueError, match="GROQ_API_KEY"):
            get_llm()

    def test_get_llm_invalid_provider_raises_error(self, monkeypatch):
        """Deve lançar ValueError para provedor inválido."""
        from shared.config import Settings

        test_settings = Settings(llm_provider="invalid")
        monkeypatch.setattr("python_chatbot.llm_provider.settings", test_settings)

        with pytest.raises(ValueError, match="não suportado"):
            get_llm()

    def test_get_llm_openai_with_key(self, monkeypatch):
        """Deve criar ChatOpenAI quando a key está configurada."""
        from shared.config import Settings

        test_settings = Settings(
            openai_api_key="fake-key-for-testing",
            llm_provider="openai",
        )
        monkeypatch.setattr("python_chatbot.llm_provider.settings", test_settings)

        llm = get_llm()
        assert llm is not None

    def test_get_llm_groq_with_key(self, monkeypatch):
        """Deve criar ChatGroq quando a key está configurada."""
        from shared.config import Settings

        test_settings = Settings(
            groq_api_key="fake-key-for-testing",
            llm_provider="groq",
        )
        monkeypatch.setattr("python_chatbot.llm_provider.settings", test_settings)

        llm = get_llm()
        assert llm is not None


# ============================================================
# Testes de exemplos de perguntas e respostas
# ============================================================


class TestExamples:
    """Testes que demonstram o funcionamento do chatbot com exemplos."""

    def test_example_create_list(self, fake_chain):
        """Exemplo: 'Como criar uma lista em Python?' deve retornar resposta válida."""
        question = "Como criar uma lista em Python?"
        response = fake_chain.invoke({"input": question, "history": []})
        assert isinstance(response, str)
        assert len(response) > 10  # Resposta deve ser detalhada

    def test_example_list_vs_tuple(self, fake_chain):
        """Exemplo: 'Qual a diferença entre lista e tupla?' deve retornar resposta válida."""
        question = "Qual a diferença entre lista e tupla?"
        response = fake_chain.invoke({"input": question, "history": []})
        assert isinstance(response, str)
        assert len(response) > 10

    def test_example_list_comprehension(self, fake_chain):
        """Exemplo: 'Como usar list comprehension?' deve retornar resposta válida."""
        question = "Como usar list comprehension?"
        response = fake_chain.invoke({"input": question, "history": []})
        assert isinstance(response, str)
        assert len(response) > 10


# ============================================================
# Testes da ChatbotChain (com memória)
# ============================================================


class TestChatbotChain:
    """Testes do chatbot com memória de conversação."""

    def test_chatbot_ask_returns_response(self, fake_llm):
        """ChatbotChain.ask deve retornar uma resposta de texto."""
        chatbot = ChatbotChain(fake_llm)
        response = chatbot.ask("Como criar uma lista em Python?")
        assert isinstance(response, str)
        assert len(response) > 0

    def test_chatbot_memory_starts_empty(self, fake_llm):
        """O histórico deve começar vazio."""
        chatbot = ChatbotChain(fake_llm)
        assert chatbot.get_history() == []

    def test_chatbot_memory_after_interaction(self, fake_llm):
        """O histórico deve conter a interação após uma pergunta."""
        chatbot = ChatbotChain(fake_llm)
        chatbot.ask("Como criar uma lista?")
        history = chatbot.get_history()
        assert len(history) == 2  # human + ai
        assert history[0][0] == "human"
        assert history[0][1] == "Como criar uma lista?"
        assert history[1][0] == "ai"

    def test_chatbot_memory_multiple_interactions(self, fake_llm):
        """O histórico deve acumular múltiplas interações."""
        chatbot = ChatbotChain(fake_llm)
        chatbot.ask("Pergunta 1")
        chatbot.ask("Pergunta 2")
        history = chatbot.get_history()
        assert len(history) == 4  # 2 human + 2 ai

    def test_chatbot_clear_memory(self, fake_llm):
        """clear_memory deve esvaziar o histórico."""
        chatbot = ChatbotChain(fake_llm)
        chatbot.ask("Como criar uma lista?")
        assert len(chatbot.get_history()) == 2
        chatbot.clear_memory()
        assert chatbot.get_history() == []
