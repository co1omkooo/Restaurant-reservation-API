from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from app.database import Base


class Reservation(Base):
    """
    Модель бронирования столика.

    Атрибуты:
        id (int): Уникальный идентификатор брони
        customer_name (str): Имя клиента
        table_id (int): ID забронированного столика
        reservation_time (DateTime): Время бронирования
        duration_minutes (int): Длительность брони в минутах
    """
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, index=True, nullable=False)
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=False)
    reservation_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
