from datetime import datetime
from pydantic import BaseModel, Field


class RollBase(BaseModel):
    length: float = Field(..., gt=0, description="Длина рулона в метрах")
    weight: float = Field(..., gt=0, description="Вес рулона в килограммах")


class Roll(RollBase):
    id: int = Field(description="Уникальный идентификатор рулона")
    created_at: datetime = Field(description="Дата добавления рулона на склад")
    removed_at: datetime | None = Field(None, description="Дата удаления рулона со склада")

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }


class RollFilter(BaseModel):
    id_min: int | None = Field(
        None,
        ge=0,
        description="Минимальный ID рулона (включительно)"
    )
    id_max: int | None = Field(
        None,
        ge=0,
        description="Максимальный ID рулона (включительно)"
    )
    weight_min: float | None = Field(
        None,
        ge=0,
        description="Минимальный вес рулона в килограммах (включительно)"
    )
    weight_max: float | None = Field(
        None,
        ge=0,
        description="Максимальный вес рулона в килограммах (включительно)"
    )
    length_min: float | None = Field(
        None,
        ge=0,
        description="Минимальная длина рулона в метрах (включительно)"
    )
    length_max: float | None = Field(
        None,
        ge=0,
        description="Максимальная длина рулона в метрах (включительно)"
    )
    created_at_min: datetime | None = Field(
        None,
        description="Минимальная дата и время добавления рулона (включительно)"
    )
    created_at_max: datetime | None = Field(
        None,
        description="Максимальная дата и время добавления рулона (включительно)"
    )
    removed_at_min: datetime | None = Field(
        None,
        description="Минимальная дата и время удаления рулона (включительно)"
    )
    removed_at_max: datetime | None = Field(
        None,
        description="Максимальная дата и время удаления рулона (включительно)"
    )