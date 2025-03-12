from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.stats.schemas import StatsResponse, StatsFilter
from src.stats.service import get_roll_stats

router = APIRouter()


@router.get("/stats/", response_model=StatsResponse)
def get_stats(
    filters: StatsFilter = Depends(),
    db: Session = Depends(get_db)
):
    stats = get_roll_stats(db=db, filters=filters)
    return stats
