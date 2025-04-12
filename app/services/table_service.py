"""
Сервисный слой для операций со столиками.

Содержит бизнес-логику управления столиками,
отделяя операции с базой данных от API эндпоинтов.
"""

from sqlalchemy.orm import Session

from app.models.table import Table
from app.schemas.table import TableCreate


def get_tables(db: Session, skip: int = 0, limit: int = 100):
    """
    Получить список столиков из базы данных с пагинацией.

    Аргументы:
        db: Сессия базы данных
        skip: Количество пропускаемых записей
        limit: Лимит возвращаемых записей

    Возвращает:
        Список объектов Table
    """
    return db.query(Table).offset(skip).limit(limit).all()


def create_table(db: Session, table: TableCreate):
    """
    Создать и сохранить новый столик в базе данных.

    Аргументы:
        db: Сессия базы данных
        table: Данные для создания столика

    Возвращает:
        Созданный объект Table

    Исключения:
        SQLAlchemyError: При ошибке операции с базой данных
    """
    db_table = Table(**table.model_dump())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table


def delete_table(db: Session, table_id: int):
    """
    Удалить столик из базы данных по ID.

    Аргументы:
        db: Сессия базы данных
        table_id: ID удаляемого столика

    Возвращает:
        Удаленный объект Table если найден, иначе None
    """
    table = db.query(Table).filter(Table.id == table_id).first()
    if table:
        db.delete(table)
        db.commit()
        return table
    return None
