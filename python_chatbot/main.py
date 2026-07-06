"""
Chatbot interativo via terminal.

Ponto de entrada da Questão 2. Permite ao usuário fazer perguntas
sobre Python e recebe respostas do LLM via Langchain.

Execução:
    python -m python_chatbot.main

Exemplo de uso:
    Você: Como criar uma lista em Python?
    Bot: Para criar uma lista em Python, você pode usar colchetes...
"""

from python_chatbot.chain import ChatbotChain
from python_chatbot.llm_provider import get_llm


def run_chatbot():
    """
    Executa o chatbot interativo no terminal.

    O loop continua até o usuário digitar '/sair'.
    Trata erros de configuração (API key ausente) e erros de execução.
    """
    print("=" * 60)
    print("  Chatbot Python — Powered by Langchain + LCEL")
    print("=" * 60)
    print()
    print("  Faça perguntas sobre programação em Python.")
    print("  Digite '/sair' para encerrar.")
    print("  Digite '/exemplos' para ver perguntas sugeridas.")
    print("-" * 60)
    print()

    # Tenta inicializar o LLM
    try:
        llm = get_llm()
    except ValueError as e:
        print(f"Erro de configuração: {e}")
        print()
        print("Para usar o chatbot:")
        print("  1. Copie .env.example para .env")
        print("  2. Configure a API key do provedor escolhido")
        print("  3. Execute novamente")
        return

    # Cria o chatbot com memória de conversação
    chatbot = ChatbotChain(llm)

    while True:
        try:
            user_input = input("Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando o chatbot. Até logo!")
            break

        if not user_input:
            continue

        if user_input.lower() == "/sair":
            print("Encerrando o chatbot. Até logo!")
            break

        if user_input.lower() == "/exemplos":
            _show_examples()
            continue

        if user_input.lower() == "/historico":
            _show_history(chatbot)
            continue

        try:
            # Processa a pergunta através da chain LCEL com memória
            response = chatbot.ask(user_input)
            print(f"Bot: {response}")
            print()
        except Exception as e:
            print(f"Erro ao processar a pergunta: {e}")
            print()


def _show_examples():
    """Exibe perguntas de exemplo para o usuário."""
    print()
    print("Perguntas sugeridas:")
    print("  • Como criar uma lista em Python?")
    print("  • Qual a diferença entre lista e tupla?")
    print("  • Como funciona o decorator em Python?")
    print("  • Como ler um arquivo CSV em Python?")
    print("  • O que é list comprehension?")
    print()


def run_demo():
    """
    Executa uma demonstração não-interativa com perguntas pré-definidas.

    Útil para validar o funcionamento do chatbot sem interação humana.
    Imprime as perguntas e respostas no terminal.
    """
    print("=" * 60)
    print("  Demonstração do Chatbot Python")
    print("=" * 60)
    print()

    try:
        llm = get_llm()
    except ValueError as e:
        print(f"Erro de configuração: {e}")
        return

    chatbot = ChatbotChain(llm)

    # Perguntas de exemplo para demonstração
    demo_questions = [
        "Como criar uma lista em Python?",
        "Qual a diferença entre lista e tupla?",
        "Como usar list comprehension?",
    ]

    for question in demo_questions:
        print(f"Pergunta: {question}")
        try:
            response = chatbot.ask(question)
            print(f"Resposta: {response}")
        except Exception as e:
            print(f"Erro: {e}")
        print("-" * 60)


if __name__ == "__main__":
    run_chatbot()
