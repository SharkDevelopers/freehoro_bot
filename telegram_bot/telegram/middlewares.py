from functools import wraps
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram_media_cache import MediaManager
from loguru import logger
from shared.storage import Database

from utils import get_db, get_media_manager


def logger_handler(handler):
    @wraps(handler)
    async def wrapper(message, *args, **kwargs):
        try:
            # Логирование перед вызовом хэндлера
            logger.debug(
                f"Handler: {handler.__name__} | User ID: {message.from_user.id}"
            )

            # Вызов исходного хэндлер
            return await handler(message, *args, **kwargs)
        except Exception as e:
            # Логирование ошибок
            logger.error(f"Error in handler {handler.__name__} | Exception: {e}")
            raise e  # Повторно выбрасываем исключение после логирования

    return wrapper


class ObjectMiddleware(BaseMiddleware):
    def __init__(self):
        self.db: Database = get_db()
        self.media_manager: MediaManager = get_media_manager()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data["db"] = self.db
        data["media_manager"] = self.media_manager
        await handler(event, data)
