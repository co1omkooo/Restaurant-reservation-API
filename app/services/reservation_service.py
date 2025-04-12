from datetime import timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate


def get_reservations(db: Session, skip: int = 0, limit: int = 100):
    """
    Получить список бронирований из базы данных с пагинацией.
    Аргументы:
        db: Сессия базы данных
        skip: Количество пропускаемых записей
        limit: Лимит возвращаемых записей
    Возвращает:
        Список объектов Reservation
    """
    return db.query(Reservation).offset(skip).limit(limit).all()


def create_reservation(db: Session, reservation: ReservationCreate):
    """
    Создать и сохранить новую бронь в базе данных.
    Аргументы:
        db: Сессия базы данных
        reservation: Данные бронирования
    Возвращает:
        Созданный объект Reservation
    Исключения:
        SQLAlchemyError: При ошибке операции с базой данных
    """
    db_reservation = Reservation(**reservation.dict())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation


def delete_reservation(db: Session, reservation_id: int):
    """
    Удалить бронь из базы данных по ID.

    Аргументы:
        db: Сессия базы данных
        reservation_id: ID удаляемой брони
    Возвращает:
        Удаленный объект Reservation если найден, иначе None
    """
    reservation = (
        db.query(Reservation).filter(Reservation.id == reservation_id).first()
    )
    if reservation:
        db.delete(reservation)
        db.commit()
        return reservation
    return None


def check_reservation_conflict(db: Session, reservation: ReservationCreate):
    """
    Проверить конфликт времени для новой брони.
    Аргументы:
        db: Сессия базы данных
        reservation: Данные новой брони
    Возвращает:
        bool: True если есть конфликт, False если нет
    """
    start_time = reservation.reservation_time
    end_time = start_time + timedelta(minutes=reservation.duration_minutes)
    conflicting = db.query(Reservation).filter(
        Reservation.table_id == reservation.table_id,
        Reservation.reservation_time < end_time,
        func.datetime(Reservation.reservation_time) +
        (Reservation.duration_minutes * func.interval('1 minute')) > start_time
    ).count()
    return conflicting > 0
