import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from loguru import logger

from stream import StreamManager
from .utils import get_stream_manager


router = APIRouter()


@router.websocket("/ws/conn/{user_name}")
async def websocket_handler(
    websocket: WebSocket,
    user_name: str,
    stream_manager: StreamManager = Depends(get_stream_manager),
):
    """
    Эндпоинт для обработки WebSocket подключений.
    """
    try:
        logger.info(f"Новое подключение: {user_name}")
        # Устанавливаем соединение через stream_manager
        await stream_manager.new_connect(websocket, user_name)

        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        # Если клиент отключается
        logger.info(f"Клиент {user_name} отключился.")
        stream_manager.disconnect(websocket)  # используем stream_manager для отключения
    except Exception as e:
        # Обработка других ошибок
        logger.error(f"Ошибка в WebSocket соединении для пользователя {user_name}: {e}")
        await websocket.close()
