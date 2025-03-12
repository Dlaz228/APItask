from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.rolls.router import router as rolls_router
from database import initialize_database
import uvicorn

app = FastAPI()


initialize_database()

app.include_router(rolls_router, prefix="/rolls", tags=["rolls"])

if __name__ == "__main__":
    uvicorn.run(app="main:app")
