import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.main import app
from src.rolls.schemas import Roll

client = TestClient(app)


@pytest.fixture
def mock_roll_service():
    with patch("src.rolls.router.create_roll") as mock_create_roll, \
         patch("src.rolls.router.get_rolls_by_filter") as mock_get_rolls, \
         patch("src.rolls.router.remove_roll") as mock_remove_roll:
        yield mock_create_roll, mock_get_rolls, mock_remove_roll


def test_create_roll(mock_roll_service):
    mock_create_roll, _, _ = mock_roll_service
    mock_create_roll.return_value = Roll(id=1, length=10.0, weight=5.0)

    response = client.post("/rolls/CreateNewRoll/", json={"length": 10.0, "weight": 5.0})

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["length"] == 10.0
    assert response.json()["weight"] == 5.0


def test_get_rolls(mock_roll_service):
    _, mock_get_rolls, _ = mock_roll_service
    mock_get_rolls.return_value = [
        Roll(id=1, length=10.0, weight=5.0),
        Roll(id=2, length=20.0, weight=10.0),
    ]

    response = client.get("/rolls/GetRolls/")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_remove_roll(mock_roll_service):
    _, _, mock_remove_roll = mock_roll_service
    mock_remove_roll.return_value = Roll(id=1, length=10.0, weight=5.0, removed_at="2023-10-01T00:00:00")

    response = client.put("/rolls/1/RemoveRoll/")

    assert response.status_code == 200
    assert response.json()["removed_at"] == "2023-10-01T00:00:00"
