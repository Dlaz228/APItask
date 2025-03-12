from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.stats.schemas import StatsResponse, StatsFilter
from src.stats.service import get_roll_stats
from src.exceptions import DatabaseError

router = APIRouter()


@router.get("/stats/", response_model=StatsResponse)
def get_stats(
    filters: StatsFilter = Depends(),
    db: Session = Depends(get_db),
):
    try:
        stats = get_roll_stats(db=db, filters=filters)
        return stats
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при расчете статистики: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Некорректные данные для расчета статистики: {str(e)}",
        )
