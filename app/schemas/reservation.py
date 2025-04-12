"""
Схемы Pydantic для валидации данных бронирований.

Определяют структуру данных для API эндпоинтов,
включая валидацию времени брони и длительности.
"""

from datetime import datetime

from pydantic import BaseModel, Field, validator

# from typing import Optional


class ReservationBase(BaseModel):
    """
    Базовая схема бронирования с общими атрибутами.

    Поля:
        customer_name: Имя клиента
        table_id: ID столика
        reservation_time: Время бронирования
        duration_minutes: Длительность брони (должна быть положительной)
    """
    customer_name: str = Field(..., example="Иван Иванов", min_length=2)
    table_id: int = Field(..., example=1, gt=0)
    reservation_time: datetime = Field(..., example="2023-12-31T19:00:00")
    duration_minutes: int = Field(..., example=90, gt=0)

    @validator('duration_minutes')
    def validate_duration(cls, duration):
        """Проверяет, что длительность положительная."""
        if duration <= 0:
            raise ValueError("Длительность должна быть положительной")
        return duration


class ReservationCreate(ReservationBase):
    """Схема для создания новых броней (наследует ReservationBase)."""
    pass


class Reservation(ReservationBase):
    """
    Полная схема бронирования, включая read-only поля.

    Добавляет:
        id: Уникальный идентификатор в базе данных
    """
    id: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "customer_name": "Иван Иванов",
                "table_id": 1,
                "reservation_time": "2023-12-31T19:00:00",
                "duration_minutes": 90
            }
        }
