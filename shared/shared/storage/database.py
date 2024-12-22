import logging
from typing import Any, Optional, Union

from motor.motor_asyncio import AsyncIOMotorClient

from .mixins import ChatMixin, UserMixin


class Database(UserMixin, ChatMixin):
    client: AsyncIOMotorClient

    def __init__(
        self,
        db_name: str,
        client: Union[AsyncIOMotorClient, Any] = None,
        uri: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
    ):
        """Инициализация класса и подключение к базе данных."""

        self.logger = logger or logging.getLogger(__name__)
        if uri and client is None:
            self.client = AsyncIOMotorClient(uri)
        else:
            self.client = client
        self.db = self.client[db_name]
        self.logger.info("Соединение с базой данных установлено.")

    @property
    def users(self):
        return self.db["users"]

    @property
    def chats(self):
        return self.db["chats"]

    def disconnect(self):
        """Закрытие подключения к MongoDB."""
        if self.client:
            self.client.close()
            self.logger.info("Соединение с базой данных закрыто.")
