"""
Настройка системы логирования для приложения.

Функция инициализирует и конфигурирует систему логирования:
- Устанавливает общий уровень логирования
- Настраивает формат вывода логов
- Добавляет обработчики для вывода в консоль
- Настраивает логирование для сторонних библиотек
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging():
    """
    Инициализация системы логирования с настройками по умолчанию.

    Настройки включают:
    - Уровень логирования: INFO
    - Формат: [ВРЕМЯ] УРОВЕНЬ|МОДУЛЬ|ФУНКЦИЯ|СТРОКА - СООБЩЕНИЕ
    - Выходные потоки: консоль (stdout) и файл (необязательно)
    - Ротация логов: при достижении 5 МБ создается новый файл, хранится 3 бэкапа

    Пример вывода:
    [2023-10-15 14:30:45] INFO|app.main|startup_event|15 - Starting up the application...
    """

    # Создаем директорию для логов, если ее нет
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Базовый форматтер
    formatter = logging.Formatter(
        fmt='[%(asctime)s] %(levelname)s|%(name)s|%(funcName)s|%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Обработчик для вывода в консоль
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Обработчик для записи в файл с ротацией
    file_handler = RotatingFileHandler(
        filename='logs/app.log',
        maxBytes=5*1024*1024,  # 5 MB
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)

    # Устанавливаем уровень логирования для корневого логгера
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Добавляем обработчики
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # Настраиваем уровень логирования для конкретных библиотек
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

    # Логирование успешной инициализации
    logger = logging.getLogger(__name__)
    logger.info("Logging system initialized")
