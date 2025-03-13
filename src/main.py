from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from src.rolls.router import router as rolls_router
from src.stats.router import router as stats_router
from src.database import initialize_database
from src.exceptions import DatabaseError
from config import settings
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
<<<<<<< HEAD
    uvicorn.run("main:app", host=settings.APP_HOST, port=settings.APP_PORT)

print(f"App running on http://{settings.APP_HOST}:{settings.APP_PORT}")


=======
    uvicorn.run(app="main:app")
>>>>>>> 0ca3adec3cbeadc6441dea5f538c023ee451649c
