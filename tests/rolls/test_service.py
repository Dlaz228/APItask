import pytest
from unittest.mock import MagicMock, patch
from src.rolls.service import remove_roll
from src.rolls.schemas import RemoveRoll
from src.rolls.models import Roll
from src.exceptions import RollNotFoundError, DatabaseError


@pytest.fixture
def mock_db_session():
    session = MagicMock()
    return session


def test_remove_roll(mock_db_session):
    mock_roll = Roll(id=1, length=10.0, weight=5.0)

    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_roll

    remove_roll_data = RemoveRoll(roll_id=1)

    removed_roll = remove_roll(mock_db_session, remove_roll_data)

    mock_db_session.query.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()

    assert removed_roll.removed_at is not None


def test_remove_roll_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None

    remove_roll_data = RemoveRoll(roll_id=1)

    with pytest.raises(RollNotFoundError):
        remove_roll(mock_db_session, remove_roll_data)


def test_remove_roll_database_error(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = Roll(id=1, length=10.0, weight=5.0)

    mock_db_session.commit.side_effect = Exception("Ошибка базы данных")

    remove_roll_data = RemoveRoll(roll_id=1)

    with pytest.raises(DatabaseError):
        remove_roll(mock_db_session, remove_roll_data)
        