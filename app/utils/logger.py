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

    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    formatter = logging.Formatter(
        fmt='[%(asctime)s] %(levelname)s|%(name)s|%(funcName)s|%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    file_handler = RotatingFileHandler(
        filename='logs/app.log',
        maxBytes=5*1024*1024,
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logger = logging.getLogger(__name__)
    logger.info("Logging system initialized")
