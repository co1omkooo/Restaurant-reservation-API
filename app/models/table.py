from sqlalchemy import Column, Integer, String

from app.database import Base


class Table(Base):
    """
    Модель столика в ресторане.

    Атрибуты:
        id (int): Уникальный идентификатор столика
        name (str): Название столика (например, "Столик 1")
        seats (int): Количество мест за столиком
        location (str): Расположение столика (например, "У окна")
    """
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    seats = Column(Integer, nullable=False)
    location = Column(String, nullable=False)
