from logging import Logger
from typing import Any, Optional

from ..models import Chat, Message


class ChatMixin:
    chats: Any
    logger: Logger

    async def create_chat(self, chat: Chat) -> Optional[Chat]:
        """Создание нового чата."""
        try:
            await self.chats.insert_one(chat.to_dict())
            self.logger.info(f"Чат с user_id {chat.user_id} успешно создан.")
            return chat
        except Exception as e:
            self.logger.error(f"Ошибка при создании чата: {e}")
            return None

    async def get_chat_by_user_id(self, user_id: int) -> Optional[Chat]:
        """Получение чата по ID пользователя."""
        try:
            data = await self.chats.find_one({"user_id": user_id})
            if data:
                self.logger.info(f"Чат с user_id {user_id} найден.")
                return Chat(**data)
            self.logger.warning(f"Чат с user_id {user_id} не найден.")
            return None
        except Exception as e:
            self.logger.error(f"Ошибка при получении чата с user_id {user_id}: {e}")
            return None

    async def add_message_to_chat(self, user_id: int, message: Message) -> bool:
        """Добавление сообщения в чат."""
        try:
            result = await self.chats.update_one(
                {"user_id": user_id}, {"$push": {"messages": message.to_dict()}}
            )
            if result.modified_count > 0:
                self.logger.info(f"Сообщение добавлено в чат с user_id {user_id}.")
                return True
            self.logger.warning(
                f"Не удалось добавить сообщение в чат с user_id {user_id}."
            )
            return False
        except Exception as e:
            self.logger.error(
                f"Ошибка при добавлении сообщения в чат с user_id {user_id}: {e}"
            )
            return False

    async def clear_chat_messages(self, user_id: int) -> bool:
        """Очистка сообщений в чате."""
        try:
            result = await self.chats.update_one(
                {"user_id": user_id}, {"$set": {"messages": []}}
            )
            if result.modified_count > 0:
                self.logger.info(f"Чат с user_id {user_id} успешно очищен.")
                return True
            self.logger.warning(f"Не удалось очистить чат с user_id {user_id}.")
            return False
        except Exception as e:
            self.logger.error(f"Ошибка при очистке чата с user_id {user_id}: {e}")
            return False

    async def get_all_chats(self) -> list[Chat]:
        """Получение всех чатов с их последними сообщениями."""
        try:
            chats = []
            cursor = self.chats.find()  # Получаем все чаты
            async for chat_data in cursor:
                chats.append(Chat(**chat_data))
            self.logger.info("Все чаты с последними сообщениями успешно получены.")
            return chats
        except Exception as e:
            self.logger.error(
                f"Ошибка при получении чатов с последними сообщениями: {e}"
            )
            return []
