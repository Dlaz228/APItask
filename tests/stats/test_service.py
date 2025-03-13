import pytest
from sqlalchemy.orm import Session
from unittest.mock import MagicMock
from src.stats.service import get_roll_stats
from src.stats.schemas import StatsFilter, StatsResponse
from src.exceptions import DatabaseError


@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)


def test_get_roll_stats_success(mock_db):
    filters = StatsFilter(start_date="2023-01-01T00:00:00", end_date="2023-12-31T23:59:59")
    mock_db.query.return_value.filter.return_value.count.return_value = 10
    mock_db.query.return_value.filter.return_value.all.return_value = []

    result = get_roll_stats(mock_db, filters)

    assert isinstance(result, StatsResponse)
    mock_db.query.assert_called()


def test_get_roll_stats_error(mock_db):
    filters = StatsFilter(start_date="2023-01-01T00:00:00", end_date="2023-12-31T23:59:59")
    mock_db.query.side_effect = Exception("Database error")

    with pytest.raises(DatabaseError):
        get_roll_stats(mock_db, filters)