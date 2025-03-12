from sqlalchemy.orm import Session
from src.rolls.models import Roll
from src.rolls.schemas import RollBase, RollFilter
from sqlalchemy import func


def create_roll(db: Session, roll: RollBase):
    db_roll = Roll(**roll.dict())

    db.add(db_roll)
    db.commit()
    db.refresh(db_roll)

    return db_roll


def get_rolls_by_filter(db: Session, filters: RollFilter, skip: int = 0, limit: int = 100):
    query = db.query(Roll)

    filter_mapping = {
        "id_min": (Roll.id >= filters.id_min if filters.id_min is not None else None),
        "id_max": (Roll.id <= filters.id_max if filters.id_max is not None else None),
        "weight_min": (Roll.weight >= filters.weight_min if filters.weight_min is not None else None),
        "weight_max": (Roll.weight <= filters.weight_max if filters.weight_max is not None else None),
        "length_min": (Roll.length >= filters.length_min if filters.length_min is not None else None),
        "length_max": (Roll.length <= filters.length_max if filters.length_max is not None else None),
        "created_at_min": (Roll.created_at >= filters.created_at_min if filters.created_at_min is not None else None),
        "created_at_max": (Roll.created_at <= filters.created_at_max if filters.created_at_max is not None else None),
        "removed_at_min": (Roll.removed_at >= filters.removed_at_min if filters.removed_at_min is not None else None),
        "removed_at_max": (Roll.removed_at <= filters.removed_at_max if filters.removed_at_max is not None else None)
    }

    filters_to_apply = [f for f in filter_mapping.values() if f is not None]
    if filters_to_apply:
        query = query.filter(*filters_to_apply)

    return query.offset(skip).limit(limit).all()


def remove_roll(db: Session, roll_id: int):
    db_roll = db.query(Roll).filter(Roll.id == roll_id).first()

    if db_roll is None:
        return None

    db_roll.removed_at = func.date_trunc('second', func.now())

    db.commit()
    db.refresh(db_roll)

    return db_roll
