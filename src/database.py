import os
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, declarative_base
from alembic import command
from alembic.config import Config
from src.config import settings
from pathlib import Path

engine = create_engine(settings.DATABASE_URL)

sync_session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def check_and_create_database():
    # URL для подключения к серверу PostgreSQL без указания базы данных
    server_url = f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}"
    engine = create_engine(server_url)

    try:
        # Проверяем, существует ли база данных
        with engine.connect() as conn:
            conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{settings.DB_NAME}'"))
    except OperationalError:
        # Если база данных не существует, создаем её
        with engine.connect() as conn:
            conn.execution_options(isolation_level="AUTOCOMMIT")
            conn.execute(text(f"CREATE DATABASE {settings.DB_NAME}"))


def check_and_create_tables():
    engine = create_engine(settings.DATABASE_URL)
    inspector = inspect(engine)

    # Проверяем, существует ли таблица 'roll'
    if 'roll' not in inspector.get_table_names():
        # Если таблица отсутствует, применяем миграции Alembic
        apply_alembic_migrations()


def apply_alembic_migrations():
    os.chdir("C:\\APItask")

    # Загружаем конфигурацию Alembic
    alembic_cfg = Config("alembic.ini")

    command.revision(alembic_cfg, autogenerate=True, message="Initial migration")

    # Применяем миграции до последней версии
    command.upgrade(alembic_cfg, "head")


def initialize_database():
    # Проверяем и создаем базу данных, если её нет
    check_and_create_database()

    # Проверяем и создаем таблицы, если их нет
    check_and_create_tables()


def get_db():
    session = sync_session_maker()
    try:
        yield session
    finally:
        session.close()
