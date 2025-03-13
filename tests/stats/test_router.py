import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.main import app
from src.stats.schemas import StatsResponse

client = TestClient(app)


@pytest.fixture
def mock_stats_service():
    with patch("src.stats.router.get_roll_stats") as mock_get_roll_stats:
        yield mock_get_roll_stats


def test_get_stats():
    mock_stats_service().return_value = StatsResponse(
        added_rolls_count=2,
        removed_rolls_count=1,
        avg_length=15.0,
        avg_weight=7.5,
        max_length=20.0,
        min_length=10.0,
        max_weight=10.0,
        min_weight=5.0,
        total_weight=15.0,
        max_time_between_add_remove="01:00:00",
        min_time_between_add_remove="00:30:00",
        max_rolls_day="2023-10-01",
        min_rolls_day="2023-10-02",
        max_weight_day="2023-10-01",
        min_weight_day="2023-10-02",
    )

    response = client.get("/stats/stats/")

    assert response.status_code == 200
    assert response.json()["added_rolls_count"] == 2
    assert response.json()["total_weight"] == 15.0
