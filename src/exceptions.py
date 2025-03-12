from fastapi import HTTPException, status


class DatabaseError(HTTPException):

    def __init__(self, detail: str = "Ошибка при работе с базой данных"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )


class RollNotFoundError(HTTPException):

    def __init__(self, roll_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Рулон с ID {roll_id} не найден",
        )