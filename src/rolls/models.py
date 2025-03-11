import datetime

from sqlalchemy import BigInteger, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Roll(Base):
    __tablename__ = "roll"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    length: Mapped[float] = mapped_column(nullable=False)
    weight: Mapped[float] = mapped_column(nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    deleted_at: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)
