"""
Роутеры API для управления бронированиями.

Содержит все эндпоинты для операций с бронированиями:
создание, просмотр и удаление броней с проверкой конфликтов.
"""

# from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.reservation import Reservation, ReservationCreate
from app.services.reservation_service import (
    get_reservations,
    create_reservation,
    delete_reservation,
    check_reservation_conflict
)

router = APIRouter(
    prefix="/reservations",
    tags=["Брони"],
    responses={404: {"description": "Не найдено"}},
)


@router.get(
    "/",
    response_model=list[Reservation],
    summary="Список всех броней",
    description="Получить список всех текущих и будущих броней."
)
def read_reservations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Получить список броней с пагинацией.

    Параметры:
        skip: Количество записей для пропуска
        limit: Максимальное количество возвращаемых записей

    Возвращает:
        Список объектов Reservation
    """
    return get_reservations(db, skip=skip, limit=limit)


@router.post(
    "/",
    response_model=Reservation,
    status_code=201,
    summary="Создать новую бронь",
    description="Забронировать столик на указанное время.",
    responses={
        400: {"description": "Конфликт времени или ошибка валидации"}
    }
)
def create_new_reservation(
    reservation: ReservationCreate,
    db: Session = Depends(get_db)
):
    """
    Создать новую бронь после проверки на конфликты.

    Параметры:
        reservation: Данные бронирования

    Возвращает:
        Созданный объект Reservation

    Исключения:
        HTTPException: 400 если время уже занято или ошибка валидации
    """
    if check_reservation_conflict(db, reservation):
        raise HTTPException(
            status_code=400,
            detail="Этот столик уже забронирован на выбранное время"
        )
    return create_reservation(db=db, reservation=reservation)


@router.delete(
    "/{reservation_id}",
    summary="Удалить бронь",
    description="Отменить существующую бронь.",
    responses={
        200: {"description": "Бронь успешно отменена"},
        404: {"description": "Бронь не найдена"}
    }
)
def remove_reservation(reservation_id: int, db: Session = Depends(get_db)):
    """
    Удалить бронь по ID.

    Параметры:
        reservation_id: ID удаляемой брони

    Возвращает:
        Сообщение об успешном удалении

    Исключения:
        HTTPException: 404 если бронь не найдена
    """
    reservation = delete_reservation(db=db, reservation_id=reservation_id)
    if reservation is None:
        raise HTTPException(status_code=404, detail="Бронь не найдена")
    return {"message": "Бронь успешно отменена"}
