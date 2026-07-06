"""
Prompts do chatbot.

Define o system prompt que especializa o LLM em responder perguntas
sobre programação em Python com explicações detalhadas e exemplos práticos.
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# System prompt que define o comportamento do chatbot
SYSTEM_PROMPT = """Você é um especialista em programação Python com anos de experiência. \
Sua função é responder perguntas sobre Python de forma clara, detalhada e prática.

Diretrizes:
1. Sempre forneça exemplos de código quando relevante.
2. Explique conceitos de forma acessível, mesmo para iniciantes.
3. Se a pergunta não for sobre Python, educadamente redirecione para o tema.
4. Inclua boas práticas e dicas quando apropriado.
5. Mantenha as respostas concisas, mas completas."""


def create_prompt() -> ChatPromptTemplate:
    """
    Cria o template de prompt usando LCEL.

    O template inclui:
    - SystemMessage: instrução de sistema que especializa o LLM em Python
    - MessagesPlaceholder: histórico da conversa (memória)
    - HumanMessage: pergunta atual do usuário

    Returns:
        ChatPromptTemplate configurado para o chatbot.
    """
    return ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
        ]
    )
