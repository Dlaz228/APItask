from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from src.rolls.router import router as rolls_router
from src.stats.router import router as stats_router
from src.database import initialize_database
from src.exceptions import DatabaseError
import uvicorn

app = FastAPI()


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


app.include_router(rolls_router, prefix="/rolls", tags=["rolls"])
app.include_router(stats_router, prefix="/stats", tags=["stats"])


@app.exception_handler(DatabaseError)
async def database_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
