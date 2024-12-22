from fastapi import WebSocket
from loguru import logger

from .models import Event


class StreamManager:
    """Класс для управления веб-сокетными соединениями и взаимодействия с клиентами."""

    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def new_connect(self, websocket: WebSocket, user: str):
        """Обрабатываем подключение нового клиента."""
        await websocket.accept()
        self.active_connections[user] = websocket
        logger.info(f"Новое соединение установлено. Тип пользователя: {user}")

    def disconnect(self, websocket: WebSocket):
        """Отключение клиента."""
        self.active_connections = {
            user: conn
            for user, conn in self.active_connections.items()
            if conn != websocket
        }
        logger.info("Клиент отключился.")

    async def notify_event(self, event: Event):
        """Отправить сообщение всем подключенным клиентам о событии."""
        for connection in self.active_connections.values():
            try:
                await connection.send_json(event.to_dict())
            except Exception as e:
                logger.error(f"Ошибка при отправке события: {e}")
                self.disconnect(connection)

    async def send_message(self, user: str, message: str):
        """Отправить сообщение конкретному пользователю через WebSocket."""
        # Проверяем, есть ли активное соединение с этим пользователем
        if user in self.active_connections:
            websocket = self.active_connections.get(user, None)
            if websocket:
                try:
                    # Отправляем сообщение клиенту
                    await websocket.send_text(message)
                    logger.info(f"Сообщение отправлено пользователю {user}: {message}")
                except Exception as e:
                    logger.error(
                        f"Ошибка при отправке сообщения пользователю {user}: {e}"
                    )
                    self.disconnect(websocket)
        else:
            logger.warning(
                f"Нет активного соединения с пользователем {user} для отправки сообщения."
            )
