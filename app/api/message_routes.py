from aiogram.client.bot import Bot
from fastapi import APIRouter, Depends, HTTPException
from aiogram.exceptions import TelegramAPIError
from aiogram.methods.send_message import SendMessage
from loguru import logger

from schemas.message import NewMessageRequest, SendMessageRequest
from shared.storage import Database
from shared.storage.models import Message, MessageType, DirectionType
from stream import StreamManager
from stream.models import Event, EventType

from .utils import get_bot, get_db, get_stream_manager


router = APIRouter()


@router.post("/send_message")
async def send_message(
    request: SendMessageRequest,
    db: Database = Depends(get_db),
    bot: Bot = Depends(get_bot),
    stream_manager: StreamManager = Depends(get_stream_manager),
):
    """
    Отправка сообщения пользователю через Telegram.
    """
    try:
        # Попытка отправить сообщение через Telegram API
        try:
            message_bot = await bot.send_message(
                chat_id=request.user_id, text=request.text
            )
            if not message_bot:
                raise TelegramAPIError(
                    message="Не удалось отправить сообщение.",
                    method=SendMessage(chat_id=request.user_id, text=request.text),
                )
        except Exception as e:
            logger.error(f"Ошибка при вызове Telegram API: {e}")
            raise HTTPException(status_code=400, detail="Ошибка Telegram API.")

        logger.info(
            f"Сообщение {message_bot.message_id} отправлено пользователю {request.user_id}: {request.text}"
        )

        # Создание объекта сообщения
        new_message = Message(
            id=message_bot.message_id,
            direction=DirectionType.outgoing,
            type=MessageType.text,
            text=request.text,
        )

        # Сохранение сообщения в базу данных
        if await db.add_message_to_chat(user_id=request.user_id, message=new_message):
            # Уведомление через StreamManager
            event = Event(
                chat_id=request.user_id,
                event_type=EventType.new_message,
                data=new_message,
            )
            await stream_manager.notify_event(event)
            return {"status": "success", "message": "Сообщение отправлено."}
        else:
            logger.warning(
                f"Не удалось сохранить сообщение для пользователя {request}."
            )
            raise HTTPException(
                status_code=500, detail="Ошибка при сохранении сообщения."
            )
    except HTTPException as http_exc:
        # Проброс ошибок HTTP с деталями
        raise http_exc
    except Exception as e:
        # Общий обработчик ошибок
        logger.error(f"Ошибка при отправке сообщения {request}: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера.")


@router.post("/new_message")
async def add_message(
    request: NewMessageRequest,
    db: Database = Depends(get_db),
    stream_manager: StreamManager = Depends(get_stream_manager),
):
    """
    Добавление сообщения в базу данных чатов.
    """
    try:
        message = Message(
            id=request.message_id,
            direction=DirectionType.incoming,
            type=MessageType.text,
            text=request.text,
        )
        success = await db.add_message_to_chat(user_id=request.user_id, message=message)
        if success:
            event = Event(
                chat_id=request.user_id,
                event_type=EventType.new_message,
                data=message,
            )
            await stream_manager.notify_event(event)
            logger.info(
                f"Сообщение {message.id} добавлено в чат для пользователя {request.user_id}."
            )
            return {"status": "success", "message": "Сообщение добавлено в чат."}
        else:
            logger.warning(
                f"Не удалось добавить сообщение для пользователя {request.user_id}."
            )
            raise HTTPException(
                status_code=400, detail="Не удалось добавить сообщение в чат."
            )
    except Exception as e:
        logger.error(
            f"Ошибка при добавлении сообщения в чат для пользователя {request.user_id}: {e}"
        )
        raise HTTPException(
            status_code=500, detail="Ошибка при добавлении сообщения в чат."
        )
