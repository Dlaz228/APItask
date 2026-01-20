import pytest
from sqlalchemy.orm import Session
from unittest.mock import MagicMock
from src.rolls.service import create_roll, get_rolls_by_filter, remove_roll
from src.rolls.schemas import RollBase, RollFilter, RemoveRoll
from src.rolls.models import RollModel
from src.rolls.schemas import Roll
from src.exceptions import DatabaseError, RollNotFoundError


@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)


def test_create_roll_success(mock_db):
    roll_data = RollBase(length=10.0, weight=5.0)
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None

    result = create_roll(mock_db, roll_data)

    assert isinstance(result, RollModel)
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


def test_create_roll_error(mock_db):
    roll_data = RollBase(length=10.0, weight=5.0)
    mock_db.add.side_effect = Exception("Database error")

    with pytest.raises(DatabaseError):
        create_roll(mock_db, roll_data)

    mock_db.rollback.assert_called_once()


def test_get_rolls_by_filter_success(mock_db):
    # Настраиваем мок для возврата списка
    mock_roll = RollModel(id=1, length=10.0, weight=5.0, created_at="2023-01-01T00:00:00")
    mock_db.query.return_value.offset.return_value.limit.return_value.all.return_value = [mock_roll]

    filters = RollFilter()
    result = get_rolls_by_filter(mock_db, filters)

    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], RollModel)


def test_get_rolls_by_filter_error(mock_db):
    filters = RollFilter()
    mock_db.query.side_effect = Exception("Database error")

    with pytest.raises(DatabaseError):
        get_rolls_by_filter(mock_db, filters)


def test_remove_roll_success(mock_db):
    roll_data = RemoveRoll(roll_id=1)
    mock_roll = MagicMock(spec=Roll)
    mock_db.query.return_value.filter.return_value.first.return_value = mock_roll

    result = remove_roll(mock_db, roll_data)

    assert result == mock_roll
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


def test_remove_roll_not_found(mock_db):
    roll_data = RemoveRoll(roll_id=1)
    mock_db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(RollNotFoundError):
        remove_roll(mock_db, roll_data)


def test_remove_roll_error(mock_db):
    roll_data = RemoveRoll(roll_id=1)
    mock_db.query.side_effect = Exception("Database error")

    with pytest.raises(DatabaseError):
        remove_roll(mock_db, roll_data)

    mock_db.rollback.assert_called_once()