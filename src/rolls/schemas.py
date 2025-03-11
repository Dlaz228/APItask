from datetime import datetime
from pydantic import BaseModel, Field


class RollBase(BaseModel):
    length: float = Field(..., gt=0, description="Длина рулона в метрах")
    weight: float = Field(..., gt=0, description="Вес рулона в килограммах")


class RollCreate(RollBase):
    pass


class RollUpdate(BaseModel):
    length: float | None = Field(None, gt=0, description="Длина рулона в метрах")
    weight: float | None = Field(None, gt=0, description="Вес рулона в килограммах")


class Roll(RollBase):
    id: int = Field(..., description="Уникальный идентификатор рулона")
    added_at: datetime = Field(..., description="Дата добавления рулона на склад")
    removed_at: datetime | None = Field(None, description="Дата удаления рулона со склада")