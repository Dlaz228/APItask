import sys
import webbrowser
import threading
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
import uvicorn


# Позволяет запускать как модуль (`python -m src.main`), так и как скрипт (`python src/main.py`)
if __package__ is None or __package__ == "":
    project_root = Path(__file__).resolve().parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

from src.rolls.router import router as rolls_router
from src.stats.router import router as stats_router
from src.database import initialize_database
from src.exceptions import DatabaseError
from src.config import settings


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
    # Открываем браузер с документацией через небольшую задержку
    def open_browser():
        import time
        time.sleep(1.5)  # Даём серверу время запуститься
        docs_url = f"http://{settings.APP_HOST}:{settings.APP_PORT}/docs"
        webbrowser.open(docs_url)
        print(f"Открыта документация: {docs_url}")
    
    # Запускаем открытие браузера в отдельном потоке
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    print(f"Запуск сервера на http://{settings.APP_HOST}:{settings.APP_PORT}")
    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT)
