from typing import Any, Dict
import aiohttp
from loguru import logger
from conf import config


class Provider:
    @staticmethod
    async def _request(url: str, data: Dict[str, Any]) -> Any:
        """
        Выполняет POST-запрос к указанному URL с передачей JSON-данных.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.debug(f"Request successful: {result}")
                        return result  # Возвращаем результат для более гибкой обработки
                    else:
                        error_message = await response.text()
                        logger.error(
                            f"Failed request: {response.status} - {error_message}"
                        )
                        return {"status": response.status, "error": error_message}
        except Exception as e:
            logger.exception(f"Error occurred while making a request: {str(e)}")
            return {"status": "error", "exception": str(e)}

    @classmethod
    async def notify_new_message(cls, user_id: int, message_id: int, text: str) -> Any:
        """
        Отправляет уведомление о новом сообщении через API.
        """
        data = {
            "user_id": user_id,
            "message_id": message_id,
            "text": text,
        }
        await cls._request(config.app_url + "/new_message", data)
