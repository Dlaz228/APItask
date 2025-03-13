import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session
from unittest.mock import MagicMock
from src.stats.router import get_stats
from src.stats.schemas import StatsFilter, StatsResponse


@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)


def test_get_stats_success(mock_db):
    filters = StatsFilter(start_date="2023-01-01T00:00:00", end_date="2023-12-31T23:59:59")
    mock_db.query.return_value.filter.return_value.count.return_value = 10
    mock_db.query.return_value.filter.return_value.all.return_value = []

    result = get_stats(filters, mock_db)

    assert isinstance(result, StatsResponse)
    mock_db.query.assert_called()


def test_get_stats_error(mock_db):
    filters = StatsFilter(start_date="2023-01-01T00:00:00", end_date="2023-12-31T23:59:59")
    mock_db.query.side_effect = Exception("Database error")

    with pytest.raises(HTTPException):
        get_stats(filters, mock_db)