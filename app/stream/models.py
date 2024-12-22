from pydantic import BaseModel
from typing import Union
from shared.storage.models import Message, Chat
from enum import Enum


class EventType(Enum):
    """Типы событий, которые могут произойти в чате."""

    new_chat = "new_chat"  # Новый чат
    new_message = "new_message"  # Новое сообщение


class Event(BaseModel):
    """Модель события, отправляемого через WebSocket."""

    chat_id: int
    event_type: EventType  # Тип события (новый чат или сообщение)
    data: Union[Chat, Message]  # Данные события (новый чат или сообщение)

    class Config:
        use_enum_values = True

    def to_dict(self):
        return {
            "user_id": self.chat_id,
            "event_type": self.event_type,
            "data": self.data.to_dict(),
        }
