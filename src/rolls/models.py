from datetime import datetime
from sqlalchemy import BigInteger, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class RollModel(Base):
    """
    Модель для таблицы 'roll'.

    Атрибуты:
        id (int): Уникальный идентификатор рулона. Используется как первичный ключ.
        length (float): Длина рулона. Не может быть NULL.
        weight (float): Вес рулона. Не может быть NULL.
        created_at (datetime): Дата и время создания записи. Устанавливается автоматически.
        removed_at (datetime | None): Дата и время удаления записи (мягкое удаление). Может быть NULL.
    """
    __tablename__ = "roll"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    length: Mapped[float] = mapped_column(nullable=False)
    weight: Mapped[float] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.date_trunc("second", func.now()),
    )
    removed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
