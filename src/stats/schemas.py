from pydantic import BaseModel, Field
from datetime import datetime, time, date


class StatsFilter(BaseModel):
    """
    Схема для фильтрации статистики.

    Атрибуты:
        start_date (datetime): Начальная дата периода.
        end_date (datetime): Конечная дата периода.
    """

    start_date: datetime = Field(..., description="Начальная дата периода")
    end_date: datetime = Field(..., description="Конечная дата периода")


class StatsResponse(BaseModel):
    """
    Схема для представления статистики.

    Атрибуты:
        added_rolls_count (int | None): Количество добавленных рулонов.
        removed_rolls_count (int | None): Количество удалённых рулонов.
        avg_length (float | None): Средняя длина рулонов.
        avg_weight (float | None): Средний вес рулонов.
        max_length (float | None): Максимальная длина рулонов.
        min_length (float | None): Минимальная длина рулонов.
        max_weight (float | None): Максимальный вес рулонов.
        min_weight (float | None): Минимальный вес рулонов.
        total_weight (float | None): Суммарный вес рулонов.
        max_time_between_add_remove (time | None): Максимальный промежуток между добавлением и удалением (в часах).
        min_time_between_add_remove (time | None): Минимальный промежуток между добавлением и удалением (в часах).
        max_rolls_day (date | None): День, когда количество рулонов на складе было максимальным.
        min_rolls_day (date | None): День, когда количество рулонов на складе было минимальным.
        max_weight_day (date | None): День, когда суммарный вес рулонов на складе был максимальным.
        min_weight_day (date | None): День, когда суммарный вес рулонов на складе был минимальным.
    """

    added_rolls_count: int | None = Field(None, description="Количество добавленных рулонов")
    removed_rolls_count: int | None = Field(None, description="Количество удалённых рулонов")
    avg_length: float | None = Field(None, description="Средняя длина рулонов")
    avg_weight: float | None = Field(None, description="Средний вес рулонов")
    max_length: float | None = Field(None, description="Максимальная длина рулонов")
    min_length: float | None = Field(None, description="Минимальная длина рулонов")
    max_weight: float | None = Field(None, description="Максимальный вес рулонов")
    min_weight: float | None = Field(None, description="Минимальный вес рулонов")
    total_weight: float | None = Field(None, description="Суммарный вес рулонов")
    max_time_between_add_remove: time | None = Field(
        None, description="Максимальный промежуток между добавлением и удалением (в часах)"
    )
    min_time_between_add_remove: time | None = Field(
        None, description="Минимальный промежуток между добавлением и удалением (в часах)"
    )
    max_rolls_day: date | None = Field(
        None, description="День, когда количество рулонов на складе было максимальным"
    )
    min_rolls_day: date | None = Field(
        None, description="День, когда количество рулонов на складе было минимальным"
    )
    max_weight_day: date | None = Field(
        None, description="День, когда суммарный вес рулонов на складе был максимальным"
    )
    min_weight_day: date | None = Field(
        None, description="День, когда суммарный вес рулонов на складе был минимальным"
    )
