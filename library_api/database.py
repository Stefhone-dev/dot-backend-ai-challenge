"""
Configuração do banco de dados SQLite.

Cria o engine do SQLAlchemy/SQLModel e fornece funções
para inicializar o schema e obter sessões.
"""

from sqlmodel import Session, SQLModel, create_engine

# Engine SQLite — arquivo local "library.db"
# check_same_thread=False permite uso com FastAPI (múltiplas threads)
sqlite_url = "sqlite:///library.db"
engine = create_engine(
    sqlite_url,
    echo=False,
    connect_args={"check_same_thread": False},
)


def init_db():
    """
    Inicializa o banco de dados criando todas as tabelas definidas
    nos modelos SQLModel registrados via metadata.
    """
    # Importa o modelo para que o SQLModel o registre antes de create_all
    from library_api.models import Book  # noqa: F401

    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Dependency do FastAPI que fornece uma sessão do banco de dados
    por requisição, garantindo o fechamento automático ao final.
    """
    with Session(engine) as session:
        yield session
