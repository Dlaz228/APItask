from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.rolls.schemas import Roll, RollBase, RollFilter, RemoveRoll
from src.rolls.service import create_roll, get_rolls_by_filter, remove_roll
from src.exceptions import DatabaseError, RollNotFoundError

router = APIRouter()


@router.post("/CreateNewRoll/", response_model=Roll)
def create_new_roll(roll: RollBase = Depends(), db: Session = Depends(get_db)):
    try:
        return create_roll(db=db, roll=roll)
    except Exception as e:
        raise DatabaseError(detail=f"Ошибка при создании рулона: {str(e)}")


@router.get("/GetRolls/", response_model=list[Roll])
def get_rolls(
    filters: RollFilter = Depends(),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    try:
        return get_rolls_by_filter(db=db, filters=filters, skip=skip, limit=limit)
    except Exception as e:
        raise DatabaseError(detail=f"Ошибка при получении рулонов: {str(e)}")


@router.put("/{roll_id}/RemoveRoll/", response_model=Roll)
def soft_remove_roll(roll: RemoveRoll = Depends(), db: Session = Depends(get_db)):
    try:
        return remove_roll(db=db, roll=roll)
    except RollNotFoundError as e:
        raise e
    except Exception as e:
        raise DatabaseError(detail=f"Ошибка при удалении рулона: {str(e)}")
