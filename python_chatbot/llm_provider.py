"""
Provider do LLM — arquitetura provider-agnostic.

Permite trocar entre OpenAI (GPT-4) e Groq (Llama 3) via variável de ambiente.
O provedor padrão é OpenAI, conforme exigido pelo desafio.

Configuração via .env:
    LLM_PROVIDER=openai    # usa ChatOpenAI com GPT-4
    LLM_PROVIDER=groq      # usa ChatGroq com Llama 3 (para testes locais)
"""

from typing import Optional

from langchain_core.language_models import BaseChatModel

from shared.config import settings


def get_llm() -> BaseChatModel:
    """
    Retorna a instância do LLM baseada na configuração do ambiente.

    Provedor padrão: OpenAI (GPT-4) — conforme exigido pelo desafio.
    Alternativa: Groq (Llama 3 70B) — para testes locais sem custo.

    Raises:
        ValueError: Se a API key do provedor selecionado não estiver configurada.
    """
    provider = settings.llm_provider.lower().strip()

    if provider == "openai":
        return _get_openai_llm()
    elif provider == "groq":
        return _get_groq_llm()
    else:
        raise ValueError(
            f"Provedor '{provider}' não suportado. "
            "Use 'openai' ou 'groq' na variável LLM_PROVIDER."
        )


def _get_openai_llm() -> BaseChatModel:
    """
    Cria instância do ChatOpenAI com GPT-4.

    Returns:
        ChatOpenAI configurado com o modelo GPT-4.
    """
    from langchain_openai import ChatOpenAI

    if not settings.openai_api_key:
        raise ValueError(
            "OPENAI_API_KEY não configurada. "
            "Defina a variável no arquivo .env ou no ambiente."
        )

    model_name = settings.llm_model or "gpt-4"
    return ChatOpenAI(
        model=model_name,
        temperature=0.7,
        api_key=settings.openai_api_key,
    )


def _get_groq_llm() -> BaseChatModel:
    """
    Cria instância do ChatGroq com Llama 3 70B.
    Alternativa gratuita para testes locais.

    Returns:
        ChatGroq configurado com o modelo Llama 3.
    """
    from langchain_groq import ChatGroq

    if not settings.groq_api_key:
        raise ValueError(
            "GROQ_API_KEY não configurada. "
            "Defina a variável no arquivo .env ou no ambiente. "
            "Crie sua key gratuita em: https://console.groq.com"
        )

    model_name = settings.llm_model or "llama-3.3-70b-versatile"
    return ChatGroq(
        model=model_name,
        temperature=0.7,
        api_key=settings.groq_api_key,
    )
