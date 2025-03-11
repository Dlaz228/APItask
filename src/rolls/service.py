from sqlalchemy.orm import Session
from src.rolls.models import Roll
from src.rolls.schemas import RollCreate


def create_roll(db: Session, roll: RollCreate):
    db_roll = Roll(**roll.dict())
    db.add(db_roll)
    db.commit()
    db.refresh(db_roll)

    return db_roll


def get_rolls(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Roll).offset(skip).limit(limit).all()
