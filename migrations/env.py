from logging.config import fileConfig
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection
from sqlalchemy.orm import sessionmaker
from alembic import context
from src.database.models import Base
from src.conf.config import config as app_config

# Это объект конфигурации Alembic, который предоставляет
# доступ к значениям в используемом файле .ini.
config = context.config

# Интерпретирует конфигурационный файл для Python логирования.
# Эта строка настраивает логгеры.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Добавьте MetaData ваших моделей здесь
# для поддержки 'autogenerate'.
target_metadata = Base.metadata
config.set_main_option("sqlalchemy.url", app_config.DB_URL)


def run_migrations_offline() -> None:
    """Запуск миграций в 'offline' режиме.

    Это настраивает контекст только с URL,
    и не требует наличия DBAPI.

    Вызовы context.execute() здесь выводят данную строку в скрипт.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations(connection: Connection):
    """Запуск миграций в 'online' режиме с использованием переданного соединения."""
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Запуск миграций в 'online' режиме с использованием синхронного движка."""
    # Используем psycopg2 для синхронных миграций
    engine = create_engine(
        app_config.DB_URL
    )  # Для миграций используем синхронное соединение
    Session = sessionmaker(bind=engine)
    with engine.connect() as connection:
        run_migrations(connection)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
