from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator
from shared.utils import TimeUtils


class DirectionType(Enum):
    incoming = "incoming"  # Входящее сообщение
    outgoing = "outgoing"  # Исходящее сообщение

    def __str__(self):
        """Преобразуем тип сообщения в строку для сериализации в JSON."""
        return self.value


class MessageType(Enum):
    photo = "photo"
    text = "text"
    video = "video"
    voice = "voice"


class Message(BaseModel):
    """
    Представление сообщения в чате.
    """

    id: int  # ID сообщения из Телеги
    direction: DirectionType  # Входящее или исходящее сообщение
    type: MessageType  # Тип сообзения
    text: str  # Текст сообщения
    created_at: TimeUtils = Field(default=TimeUtils())

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

    class Config:
        use_enum_values = True
        arbitrary_types_allowed = True

    def to_dict(self) -> dict:
        """
        Перобразование в dict
        """
        return {
            "id": self.id,
            "direction": str(self.direction),  # Преобразуем DirectionType в строку
            "type": str(self.type),  # Преобразуем MessageType в строку
            "text": self.text,
            "created_at": str(self.created_at),
        }
