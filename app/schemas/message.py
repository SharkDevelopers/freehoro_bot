from typing import Optional
from pydantic import BaseModel, Field


class SendMessageRequest(BaseModel):
    """
    Схема для отправки сообщения.
    """

    user_id: int = Field(..., gt=0, description="Идентификатор пользователя")
    text: str = Field(..., description="Текст сообщения")

    class Config:
        json_schema_extra = {"example": {"user_id": 123456, "text": "Hello, world!"}}


class NewMessageRequest(BaseModel):
    """
    Схема для добавления нового сообщения в базу данных.
    """

    user_id: int = Field(..., gt=0, description="Идентификатор пользователя Telegram")
    message_id: int = Field(..., gt=0, description="Идентификатор сообщения")
    text: str = Field(..., description="Текст сообщения")

    class Config:
        json_schema_extra = {
            "example": {"user_id": 123456, "message_id": 78910, "text": "Hello, world!"}
        }
