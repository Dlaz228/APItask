from sqlalchemy.orm import Session
from sqlalchemy import func
from src.rolls.models import RollModel
from src.rolls.schemas import RollBase, RollFilter, RemoveRoll
from src.exceptions import DatabaseError, RollNotFoundError


def create_roll(db: Session, roll: RollBase):
    try:
        db_roll = RollModel(**roll.dict())
        db.add(db_roll)
        db.commit()
        db.refresh(db_roll)
        return db_roll
    except Exception as e:
        db.rollback()
        raise DatabaseError(detail=f"Ошибка при создании рулона: {str(e)}")


def get_rolls_by_filter(db: Session, filters: RollFilter, skip: int = 0, limit: int = 100):
    try:
        query = db.query(RollModel)

        filter_mapping = {
            "id_min": (RollModel.id >= filters.id_min if filters.id_min is not None else None),
            "id_max": (RollModel.id <= filters.id_max if filters.id_max is not None else None),
            "weight_min": (RollModel.weight >= filters.weight_min if filters.weight_min is not None else None),
            "weight_max": (RollModel.weight <= filters.weight_max if filters.weight_max is not None else None),
            "length_min": (RollModel.length >= filters.length_min if filters.length_min is not None else None),
            "length_max": (RollModel.length <= filters.length_max if filters.length_max is not None else None),
            "created_at_min": (
                RollModel.created_at >= filters.created_at_min if filters.created_at_min is not None else None),
            "created_at_max": (
                RollModel.created_at <= filters.created_at_max if filters.created_at_max is not None else None),
            "removed_at_min": (
                RollModel.removed_at >= filters.removed_at_min if filters.removed_at_min is not None else None),
            "removed_at_max": (
                RollModel.removed_at <= filters.removed_at_max if filters.removed_at_max is not None else None),
        }

        filters_to_apply = [f for f in filter_mapping.values() if f is not None]
        if filters_to_apply:
            query = query.filter(*filters_to_apply)

        return query.offset(skip).limit(limit).all()
    except Exception as e:
        raise DatabaseError(detail=f"Ошибка при получении рулонов: {str(e)}")


def remove_roll(db: Session, roll: RemoveRoll):
    try:
        db_roll = db.query(RollModel).filter(RollModel.id == roll.roll_id).first()

        if db_roll is None:
            raise RollNotFoundError(roll_id=roll.roll_id)

        db_roll.removed_at = func.date_trunc("second", func.now())
        db.commit()
        db.refresh(db_roll)
        return db_roll
    except RollNotFoundError:
        raise
    except Exception as e:
        db.rollback()
        raise DatabaseError(detail=f"Ошибка при удалении рулона: {str(e)}")
