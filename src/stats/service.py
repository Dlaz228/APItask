from sqlalchemy.orm import Session
from src.rolls.models import Roll
from .schemas import StatsFilter, StatsResponse
from typing import List, Callable
from datetime import date, timedelta, time


def calculate_stats(data: List[float], operation: Callable[[List[float]], float], default: float = 0) -> float:
    return round(operation(data) if data else default, 2)


def calculate_avg(data: List[float], default: float = 0) -> float:
    return round(sum(data) / len(data), 2) if data else default


def hours_to_time(seconds: float) -> time | None:
    if seconds is None:
        return None

    rounded_seconds = round(seconds)
    hours = rounded_seconds // 3600
    remaining_seconds = rounded_seconds % 3600
    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60

    return time(hour=hours, minute=minutes, second=seconds)


def calculate_daily_and_weight_stats(rolls: List[Roll]) -> dict[date, dict[str, float]]:
    daily_stats = {}

    for roll in rolls:
        current_day = roll.created_at.date()
        removed_day = roll.removed_at.date() if roll.removed_at else None

        while current_day <= removed_day:
            if current_day not in daily_stats:
                daily_stats[current_day] = {"rolls_count": 0, "total_weight": 0.0}
            daily_stats[current_day]["rolls_count"] += 1
            daily_stats[current_day]["total_weight"] += roll.weight
            current_day += timedelta(days=1)

    return daily_stats


def get_filtered_days(stats: dict[date, dict[str, float]], key: str) -> tuple[date | None, date | None]:
    if not stats:
        return None, None

    min_day = min(stats.items(), key=lambda x: x[1][key])[0]
    max_day = max(stats.items(), key=lambda x: x[1][key])[0]
    return min_day, max_day


def get_roll_stats(db: Session, filters: StatsFilter) -> StatsResponse:
    added_rolls_count = db.query(Roll).filter(
        Roll.created_at >= filters.start_date,
        Roll.created_at <= filters.end_date
    ).count()

    removed_rolls_count = db.query(Roll).filter(
        Roll.removed_at >= filters.start_date,
        Roll.removed_at <= filters.end_date
    ).count()

    rolls_in_period = db.query(Roll).filter(
        Roll.created_at >= filters.start_date,
        Roll.removed_at < filters.end_date
    ).all()

    lengths = [roll.length for roll in rolls_in_period]
    weights = [roll.weight for roll in rolls_in_period]

    avg_length = calculate_avg(lengths)
    avg_weight = calculate_avg(weights)

    max_length = calculate_stats(lengths, max)
    min_length = calculate_stats(lengths, min)
    max_weight = calculate_stats(weights, max)
    min_weight = calculate_stats(weights, min)

    total_weight = calculate_stats(weights, sum)

    time_diffs = [
        (roll.removed_at - roll.created_at).total_seconds()
        for roll in rolls_in_period
        if roll.removed_at is not None
    ]
    max_time_between_add_remove = hours_to_time(calculate_stats(time_diffs, max, default=0.0))
    min_time_between_add_remove = hours_to_time(calculate_stats(time_diffs, min, default=0.0))

    daily_stats = calculate_daily_and_weight_stats(rolls_in_period)

    min_rolls_day, max_rolls_day = get_filtered_days(daily_stats, "rolls_count")
    min_weight_day, max_weight_day = get_filtered_days(daily_stats, "total_weight")

    return StatsResponse(
        added_rolls_count=added_rolls_count,
        removed_rolls_count=removed_rolls_count,
        avg_length=avg_length,
        avg_weight=avg_weight,
        max_length=max_length,
        min_length=min_length,
        max_weight=max_weight,
        min_weight=min_weight,
        total_weight=total_weight,
        max_time_between_add_remove=max_time_between_add_remove,
        min_time_between_add_remove=min_time_between_add_remove,
        max_rolls_day=max_rolls_day,
        min_rolls_day=min_rolls_day,
        max_weight_day=max_weight_day,
        min_weight_day=min_weight_day,
    )
