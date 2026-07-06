"""
Chain do chatbot usando LangChain Expression Language (LCEL).

Constrói a chain que conecta o prompt template, o LLM e o parser
de saída, incluindo memória de conversação para manter contexto.

LCEL permite composição declarativa via operador pipe (|):
    prompt | llm | output_parser
"""

from typing import List, Tuple

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory

from python_chatbot.prompts import create_prompt


def create_simple_chain(llm: BaseChatModel):
    """
    Cria uma chain LCEL simples sem memória, para testes unitários.

    A chain segue o fluxo:
        prompt | llm | output_parser

    Args:
        llm: Instância do modelo de linguagem.

    Returns:
        Chain LCEL executável (prompt | llm | parser).
    """
    prompt = create_prompt()
    output_parser = StrOutputParser()
    return prompt | llm | output_parser


class ChatbotChain:
    """
    Chatbot com memória de conversação usando LCEL.

    Mantém o histórico da conversa em memória (ConversationBufferMemory)
    e usa a chain LCEL (prompt | llm | parser) para gerar respostas.

    Uso:
        chatbot = ChatbotChain(llm)
        resposta = chatbot.ask("Como criar uma lista em Python?")
    """

    def __init__(self, llm: BaseChatModel):
        """
        Inicializa o chatbot com o LLM fornecido.

        Args:
            llm: Instância do modelo de linguagem (ChatOpenAI, ChatGroq, etc.)
        """
        self.llm = llm
        self.chain = create_simple_chain(llm)
        self.memory = ConversationBufferMemory(
            memory_key="history",
            return_messages=True,
        )

    def ask(self, user_input: str) -> str:
        """
        Processa a pergunta do usuário e retorna a resposta do LLM.

        Mantém o histórico da conversa na memória, permitindo
        que o chatbot lembre de perguntas e respostas anteriores.

        Args:
            user_input: Pergunta do usuário.

        Returns:
            Resposta do LLM como string.
        """
        # Obtém o histórico atual da memória
        history = self.memory.chat_memory.messages

        # Executa a chain com o input e o histórico
        response = self.chain.invoke({
            "input": user_input,
            "history": history,
        })

        # Atualiza a memória com a nova interação
        self.memory.chat_memory.add_user_message(user_input)
        self.memory.chat_memory.add_ai_message(response)

        return response

    def get_history(self) -> List[Tuple[str, str]]:
        """
        Retorna o histórico da conversa como lista de tuplas (role, content).

        Returns:
            Lista de tuplas no formato ("human", content) ou ("ai", content).
        """
        history = []
        for msg in self.memory.chat_memory.messages:
            if isinstance(msg, HumanMessage):
                history.append(("human", msg.content))
            elif isinstance(msg, AIMessage):
                history.append(("ai", msg.content))
        return history

    def clear_memory(self):
        """Limpa o histórico da conversa."""
        self.memory.clear()
