from sqlalchemy.orm import Session
from src.rolls.models import Roll
from src.rolls.schemas import RollCreate
from sqlalchemy import func


def create_roll(db: Session, roll: RollCreate):
    db_roll = Roll(**roll.dict())
    db.add(db_roll)
    db.commit()
    db.refresh(db_roll)

    return db_roll


def get_rolls(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Roll).offset(skip).limit(limit).all()


def remove_roll(db: Session, roll_id: int):
    db_roll = db.query(Roll).filter(Roll.id == roll_id).first()

    if db_roll is None:
        return None

    db_roll.removed_at = func.date_trunc('second', func.now())

    db.commit()
    db.refresh(db_roll)

    return db_roll
