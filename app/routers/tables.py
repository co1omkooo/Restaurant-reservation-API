"""
Роутеры API для управления столиками.

Содержит все эндпоинты для операций со столиками:
создание, просмотр и удаление столиков.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.table import Table, TableCreate
from app.services.table_service import get_tables, create_table, delete_table


router = APIRouter(
    prefix="/tables",
    tags=["Столики"],
    responses={404: {"description": "Не найдено"}},
)


@router.get(
    "/",
    response_model=list[Table],
    summary="Список всех столиков",
    description="Получить список всех доступных столиков в ресторане."
)
def read_tables(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получить список столиков с пагинацией.

    Параметры:
        skip: Количество записей для пропуска (для пагинации)
        limit: Максимальное количество возвращаемых записей

    Возвращает:
        Список объектов Table
    """
    tables = get_tables(db, skip=skip, limit=limit)
    return tables


@router.post(
    "/",
    response_model=Table,
    status_code=201,
    summary="Создать новый столик",
    description="Добавить новый столик в ресторан."
)
def create_new_table(table: TableCreate, db: Session = Depends(get_db)):
    """
    Создать новый столик.

    Параметры:
        table: Данные для создания столика

    Возвращает:
        Созданный объект Table

    Исключения:
        HTTPException: Если не удалось создать столик
    """
    return create_table(db=db, table=table)


@router.delete(
    "/{table_id}",
    summary="Удалить столик",
    description="Удалить столик из ресторана.",
    responses={
        200: {"description": "Столик успешно удален"},
        404: {"description": "Столик не найден"}
    }
)
def remove_table(table_id: int, db: Session = Depends(get_db)):
    """
    Удалить столик по ID.

    Параметры:
        table_id: ID удаляемого столика

    Возвращает:
        Сообщение об успешном удалении

    Исключения:
        HTTPException: 404 если столик не найден
    """
    table = delete_table(db=db, table_id=table_id)
    if table is None:
        raise HTTPException(status_code=404, detail="Столик не найден")
    return {"message": "Столик успешно удален"}
