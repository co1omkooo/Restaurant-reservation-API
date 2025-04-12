import os

from logging.config import fileConfig
from sqlalchemy import create_engine
from alembic import context

from database import Base


config = context.config
fileConfig(config.config_file_name) if config.config_file_name else None
target_metadata = Base.metadata


def get_database_url():
    """Получаем URL из тех же источников, что и основное приложение"""
    return os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@db:5432/restaurant"
    )


def run_migrations_offline():
    """Режим генерации миграций (без подключения к БД)"""
    context.configure(
        url=get_database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Режим применения миграций (с подключением к БД)"""
    connectable = create_engine(get_database_url())
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
