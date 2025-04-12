"""
Конфигурация базы данных и управление сессиями.

Этот модуль настраивает подключение к базе данных и предоставляет
утилиты для управления сессиями базы данных.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# URL подключения к базе данных из переменных окружения
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://user:password@db:5432/restaurant"
)

# Экземпляр движка базы данных
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Фабрика сессий для создания сессий базы данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для всех моделей базы данных
Base = declarative_base()


def get_db():
    """
    Функция-зависимость, которая предоставляет сессии базы данных.

    Возвращает:
        Session: Сессия базы данных

    Примечание:
        Всегда закрывает сессию после использования
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
