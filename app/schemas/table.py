"""
Схемы Pydantic для валидации данных столиков.

Определяют структуру данных для API эндпоинтов,
обеспечивают валидацию и документацию.
"""

from pydantic import BaseModel, Field
# from typing import Optional


class TableBase(BaseModel):
    """
    Базовая схема столика с общими атрибутами.

    Поля:
        name: Уникальное название столика
        seats: Количество мест (должно быть положительным)
        location: Описание расположения
    """
    name: str = Field(..., example="Столик 1", min_length=2)
    seats: int = Field(..., example=4, gt=0)
    location: str = Field(..., example="У окна", min_length=2)


class TableCreate(TableBase):
    """Схема для создания новых столиков (наследует TableBase)."""
    pass


class Table(TableBase):
    """
    Полная схема столика, включая read-only поля.

    Добавляет:
        id: Уникальный идентификатор в базе данных
    """
    id: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Столик 1",
                "seats": 4,
                "location": "У окна"
            }
        }
