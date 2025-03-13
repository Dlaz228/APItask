from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from src.rolls.router import router as rolls_router
from src.stats.router import router as stats_router
from src.database import initialize_database
from src.exceptions import DatabaseError
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        initialize_database()
    except DatabaseError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при инициализации базы данных: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Неизвестная ошибка при инициализации базы данных: {str(e)}",
        )
    yield
    print("Приложение завершает работу...")

app = FastAPI(lifespan=lifespan)

app.include_router(rolls_router, prefix="/rolls", tags=["rolls"])
app.include_router(stats_router, prefix="/stats", tags=["stats"])

if __name__ == "__main__":
    uvicorn.run(app="main:app")
