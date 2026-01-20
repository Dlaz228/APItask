from pydantic_settings import BaseSettings
from pathlib import Path
from pydantic import ValidationError

env_path = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """
    Настройки приложения, загружаемые из переменных окружения.

    Атрибуты:
        DB_PATH (str): Путь к файлу базы данных SQLite (по умолчанию database.db в корне проекта).
        APP_HOST (str): Хост приложения.
        APP_PORT (int): Порт приложения.

    Методы:
        DATABASE_URL: Возвращает строку подключения к базе данных SQLite.
    """

    DB_PATH: str = "database.db"
    APP_HOST: str
    APP_PORT: int

    @property
    def DATABASE_URL(self) -> str:
        # SQLite создает файл автоматически, если его нет
        db_file = Path(env_path) / self.DB_PATH
        return f"sqlite:///{db_file}"

    class Config:
        env_file = f"{env_path}/.env"


try:
    settings = Settings()
except ValidationError as e:
    raise e
except Exception as e:
    raise e