from pydantic_settings import BaseSettings
from pathlib import Path
from pydantic import ValidationError

env_path = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """
    Настройки приложения, загружаемые из переменных окружения.

    Атрибуты:
        DB_HOST (str): Хост базы данных.
        DB_PORT (str): Порт базы данных.
        DB_USER (str): Имя пользователя базы данных.
        DB_PASS (str): Пароль пользователя базы данных.
        DB_NAME (str): Название базы данных.

    Методы:
        DATABASE_URL: Возвращает строку подключения к базе данных.
    """

    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    APP_HOST: str
    APP_PORT: int

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = f"{env_path}/.env"


try:
    settings = Settings()
except ValidationError as e:
    raise e
except Exception as e:
    raise e