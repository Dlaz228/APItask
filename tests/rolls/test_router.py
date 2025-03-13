import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session
from unittest.mock import MagicMock
from src.rolls.models import RollModel
from src.rolls.router import create_new_roll, get_rolls, soft_remove_roll
from src.rolls.schemas import RollBase, RollFilter, RemoveRoll, Roll
from src.rolls.service import create_roll, get_rolls_by_filter, remove_roll
from src.exceptions import DatabaseError, RollNotFoundError


@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)


def test_create_new_roll_success(mock_db):
    roll_data = RollBase(length=10.0, weight=5.0)
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None

    result = create_new_roll(roll_data, mock_db)

    assert isinstance(result, RollModel)
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


def test_create_new_roll_error(mock_db):
    roll_data = RollBase(length=10.0, weight=5.0)
    mock_db.add.side_effect = Exception("Database error")

    with pytest.raises(HTTPException):
        create_new_roll(roll_data, mock_db)

    mock_db.rollback.assert_called_once()


def test_get_rolls_success(mock_db):
    # Настраиваем мок для возврата списка
    mock_roll = RollModel(id=1, length=10.0, weight=5.0, created_at="2023-01-01T00:00:00",
                          removed_at="2023-02-01T00:00:00")
    mock_roll2 = RollModel(id=2, length=10.0, weight=5.0, created_at="2023-01-01T00:00:00",
                          removed_at="2023-02-01T00:00:00")
    mock_db.query.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = [
        mock_roll, mock_roll2]

    filters = RollFilter()
    result = get_rolls(filters, mock_db)

    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], Roll)


def test_get_rolls_error(mock_db):
    filters = RollFilter()
    mock_db.query.side_effect = Exception("Database error")

    with pytest.raises(HTTPException):
        get_rolls(filters, 0, 100, mock_db)


def test_soft_remove_roll_success(mock_db):
    roll_data = RemoveRoll(roll_id=1)
    mock_roll = MagicMock(spec=RollModel)
    mock_db.query.return_value.filter.return_value.first.return_value = mock_roll

    result = soft_remove_roll(roll_data, mock_db)

    assert result == mock_roll
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


def test_soft_remove_roll_not_found(mock_db):
    roll_data = RemoveRoll(roll_id=1)
    mock_db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(RollNotFoundError):
        soft_remove_roll(roll_data, mock_db)


def test_soft_remove_roll_error(mock_db):
    roll_data = RemoveRoll(roll_id=1)
    mock_db.query.side_effect = Exception("Database error")

    with pytest.raises(HTTPException):
        soft_remove_roll(roll_data, mock_db)

    mock_db.rollback.assert_called_once()
