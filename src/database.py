import os
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.orm import sessionmaker, declarative_base
from alembic import command
from alembic.config import Config
from src.config import settings
from src.exceptions import DatabaseError

engine = create_engine(settings.DATABASE_URL)

sync_session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def check_and_create_database():
    server_url = f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}"

    try:
        engine = create_engine(server_url)
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{settings.DB_NAME}'"))
            if not result.scalar():
                conn.execution_options(isolation_level="AUTOCOMMIT")
                conn.execute(text(f"CREATE DATABASE {settings.DB_NAME}"))
    except OperationalError as e:
        raise DatabaseError(detail=f"Ошибка при проверке или создании базы данных: {str(e)}")
    except Exception as e:
        raise DatabaseError(detail=f"Неизвестная ошибка при работе с базой данных: {str(e)}")


def check_and_create_tables():
    try:
        engine = create_engine(settings.DATABASE_URL)
        inspector = inspect(engine)

        if 'roll' not in inspector.get_table_names():
            apply_alembic_migrations()
    except OperationalError as e:
        raise DatabaseError(detail=f"Ошибка при проверке или создании таблиц: {str(e)}")
    except Exception as e:
        raise DatabaseError(detail=f"Неизвестная ошибка при работе с таблицами: {str(e)}")


def apply_alembic_migrations():
    try:
        os.chdir("C:\\APItask")

        alembic_cfg = Config("alembic.ini")

        command.revision(alembic_cfg, autogenerate=True, message="Initial migration")

        command.upgrade(alembic_cfg, "head")
    except Exception as e:
        raise DatabaseError(detail=f"Ошибка при применении миграций Alembic: {str(e)}")


def initialize_database():
    try:
        check_and_create_database()

        check_and_create_tables()
    except DatabaseError as e:
        raise e
    except Exception as e:
        raise DatabaseError(detail=f"Неизвестная ошибка при инициализации базы данных: {str(e)}")


def get_db():
    session = sync_session_maker()
    try:
        yield session
    except SQLAlchemyError as e:
        raise DatabaseError(detail=f"Ошибка при работе с сессией базы данных: {str(e)}")
    finally:
        session.close()
