import pytest
from unittest.mock import MagicMock, patch
from src.stats.service import get_roll_stats
from src.stats.schemas import StatsFilter
from src.rolls.models import Roll


@pytest.fixture
def mock_db_session():
    session = MagicMock()
    return session


def test_get_roll_stats(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.count.side_effect = [2, 1]
    mock_db_session.query.return_value.filter.return_value.all.return_value = [
        Roll(length=10.0, weight=5.0, created_at="2023-10-01T00:00:00", removed_at="2023-10-02T00:00:00"),
        Roll(length=20.0, weight=10.0, created_at="2023-10-01T00:00:00", removed_at="2023-10-03T00:00:00"),
    ]

    filters = StatsFilter(start_date="2023-10-01T00:00:00", end_date="2023-10-04T00:00:00")
    stats = get_roll_stats(mock_db_session, filters)

    assert stats["added_rolls_count"] == 2
    assert stats["removed_rolls_count"] == 1
    assert stats["total_weight"] == 15.0