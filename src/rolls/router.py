from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.rolls.schemas import Roll, RollCreate
from src.rolls.service import create_roll, get_rolls

router = APIRouter()


@router.post("/CreateNewRoll/", response_model=Roll)
def create_new_roll(roll: RollCreate, db: Session = Depends(get_db)):
    return create_roll(db=db, roll=roll)


@router.get("/GetRolls/", response_model=list[Roll])
def read_rolls(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_rolls(db=db, skip=skip, limit=limit)
