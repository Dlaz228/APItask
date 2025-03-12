from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.rolls.schemas import Roll, RollBase, RollFilter
from src.rolls.service import create_roll, get_rolls_by_filter, remove_roll

router = APIRouter()


@router.post("/CreateNewRoll/", response_model=Roll)
def create_new_roll(roll: RollBase = Depends(), db: Session = Depends(get_db)):
    return create_roll(db=db, roll=roll)


@router.get("/GetRolls/", response_model=list[Roll])
def get_rolls(
    filters: RollFilter = Depends(),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return get_rolls_by_filter(db=db, filters=filters, skip=skip, limit=limit)


@router.put("/{roll_id}/RemoveRoll/", response_model=Roll)
def soft_remove_roll(roll_id: int, db: Session = Depends(get_db)):
    return remove_roll(db=db, roll_id=roll_id)
