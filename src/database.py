from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.orm import sessionmaker, declarative_base
from src.config import settings
from src.exceptions import DatabaseError
from sqlalchemy.pool import StaticPool

def _make_engine():
    # SQLite: корректные настройки для работы в FastAPI (несколько потоков/соединений)
    if settings.DATABASE_URL.startswith("sqlite:///"):
        return create_engine(
            settings.DATABASE_URL,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
    return create_engine(settings.DATABASE_URL)


engine = _make_engine()

sync_session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def check_and_create_database():
    # SQLite создает файл базы данных автоматически при первом подключении
    # Просто проверяем, что можем подключиться
    try:
        engine = _make_engine()
        # Проверяем подключение
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print(f"База данных SQLite готова к использованию: {settings.DB_PATH}")
    except OperationalError as e:
        raise DatabaseError(detail=f"Ошибка при подключении к базе данных: {str(e)}")
    except Exception as e:
        raise DatabaseError(detail=f"Неизвестная ошибка при работе с базой данных: {str(e)}")


def check_and_create_tables():
    try:
        engine = _make_engine()
        inspector = inspect(engine)

        if 'roll' not in inspector.get_table_names():
            # Для SQLite не используем Alembic на старте приложения:
            # просто создаём таблицы из SQLAlchemy моделей.
            Base.metadata.create_all(bind=engine)
    except OperationalError as e:
        raise DatabaseError(detail=f"Ошибка при проверке или создании таблиц: {str(e)}")
    except Exception as e:
        raise DatabaseError(detail=f"Неизвестная ошибка при работе с таблицами: {str(e)}")


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
