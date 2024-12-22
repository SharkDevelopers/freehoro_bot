from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator
from shared.utils import TimeUtils


class User(BaseModel):
    """
    Представление пользователя в чате.
    """

    id: int  # Chat_id в Телеграм
    full_name: Optional[str] = None  # Полное имя пользователя
    username: Optional[str] = None  # Username пользователя
    created_at: TimeUtils = Field(default=TimeUtils())
    metadata: dict = Field(default={})
    have_chat: bool = Field(default=False)

    class Config:
        arbitrary_types_allowed = True

    @field_validator("created_at", mode="before")
    def parse_created_at(cls, v):
        """
        Кастомный валидатор, который будет вызываться при загрузке данных.
        Преобразует строку или datetime в объект TimeUtils.
        """
        if v is None:
            return TimeUtils()  # Если None, берем текущее время
        elif isinstance(v, datetime):
            return TimeUtils(v)  # Если передан datetime, передаем его в TimeUtils
        elif isinstance(v, str):
            return TimeUtils.from_string(v)
        elif isinstance(v, TimeUtils):
            return v
        else:
            raise ValueError(f"Invalid value for created_at: {v}")

    def to_dict(self) -> dict:
        """
        Перобразование в dict
        """
        return {
            "id": self.id,
            "full_name": self.full_name,
            "username": self.username,
            "created_at": str(self.created_at),
            "have_chat": self.have_chat,
        }
