from typing import Optional
from pydantic import BaseModel, Field


class NewChatRequest(BaseModel):
    """
    Схема для создания нового чата.
    """

    user_id: int = Field(..., gt=0, description="Идентификатор пользователя Telegram")
    full_name: Optional[str] = Field(None, description="Полное имя пользователя")
    username: Optional[str] = Field(None, description="Имя пользователя в Telegram")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 123456,
                "full_name": "Test Test",
                "username": "testuser",
            }
        }
