"""
Configuração centralizada do projeto.

Utiliza pydantic-settings para carregar variáveis de ambiente
de forma tipada e segura.
"""

from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Settings globais do projeto carregadas via variáveis de ambiente.
    Lê automaticamente do arquivo .env se presente.
    """

    # --- Questão 2: Configuração do LLM ---
    # Provedor padrão: "openai" (exigido pelo desafio)
    # Alternativa para testes locais: "groq"
    llm_provider: str = "openai"

    # API keys
    openai_api_key: Optional[str] = None
    groq_api_key: Optional[str] = None

    # Modelo do LLM (opcional — usa padrão do provedor se vazio)
    llm_model: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


# Instância singleton das configurações
settings = Settings()
