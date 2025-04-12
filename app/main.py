"""
Главный модуль приложения FastAPI.

Этот модуль создает и настраивает экземпляр приложения FastAPI,
настраивает логирование и подключает все роутеры API.
"""

import logging

from fastapi import FastAPI

from app.routers import tables, reservations
from app.utils.logger import setup_logging

# Инициализация логирования
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="API для бронирования столиков",
    version="1.0.0",
    description="Система управления бронированием столиков в ресторане",
    contact={
        "name": "Поддержка API",
        "email": "support@restaurant.ru",
    },
)

# Подключение роутеров API
app.include_router(tables.router, tags=["Столики"])
app.include_router(reservations.router, tags=["Брони"])


@app.on_event("startup")
async def startup_event():
    """Инициализация сервисов при запуске приложения."""
    logger.info("Запуск приложения...")


@app.on_event("shutdown")
async def shutdown_event():
    """Очистка ресурсов при завершении работы."""
    logger.info("Завершение работы приложения...")
