from typing import Optional

from pydantic import BaseModel, Field

from .message import Message


class Chat(BaseModel):
    """
    Представление чата между пользователем и ботом.
    """

    user_id: int  # ID пользователя
    full_name: Optional[str] = None  # Полное имя пользователя
    username: Optional[str] = None  # Username пользователя
    messages: list[Message] = Field(default=[])  # История сообщений

    class Config:
        # Автоматическое преобразование объектов Enum в строки
        use_enum_values = True
        arbitrary_types_allowed = True

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "full_name": self.full_name,
            "username": self.username,
            "messages": [message.to_dict() for message in self.messages],
        }
