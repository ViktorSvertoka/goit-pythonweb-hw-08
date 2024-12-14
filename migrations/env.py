from logging.config import fileConfig
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection
from sqlalchemy.orm import sessionmaker
from alembic import context
from src.database.models import Base
from src.conf.config import config as app_config


config = context.config


if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = Base.metadata
config.set_main_option("sqlalchemy.url", app_config.DB_URL)


def run_migrations_offline() -> None:

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

    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:

    engine = create_engine(app_config.DB_URL)
    Session = sessionmaker(bind=engine)
    with engine.connect() as connection:
        run_migrations(connection)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
