from fastapi import APIRouter, Depends, HTTPException
from loguru import logger

from schemas.chat import NewChatRequest
from shared.storage import Database
from shared.storage.models import Chat
from stream import StreamManager
from stream.models import Event, EventType

from .utils import get_db, get_stream_manager


router = APIRouter()


@router.post("/new_chat")
async def new_chat(
    request: NewChatRequest,
    db: Database = Depends(get_db),
    stream_manager: StreamManager = Depends(get_stream_manager),
):
    """
    Создание нового чата для пользователя.
    """
    try:
        # Проверяем, существует ли пользователь
        existing_user = await db.get_user_by_id(request.user_id)
        if not existing_user:
            logger.warning(f"Пользователь с ID {request.user_id} не найден.")
            raise HTTPException(status_code=404, detail="Пользователь не найден.")

        # Создаем новый чат
        new_chat = Chat(
            user_id=request.user_id,
            full_name=request.full_name,
            username=request.username,
        )

        success = await db.create_chat(chat=new_chat)
        if success:
            event = Event(
                chat_id=request.user_id,
                event_type=EventType.new_chat,
                data=new_chat,
            )
            await stream_manager.notify_event(event)
            logger.info(f"Новый чат создан для пользователя {request.user_id}.")
            return {"status": "success", "message": "Чат успешно создан."}
        else:
            logger.warning(
                f"Не удалось создать чат для пользователя {request.user_id}."
            )
            raise HTTPException(status_code=400, detail="Не удалось создать чат.")
    except Exception as e:
        logger.error(
            f"Ошибка при создании чата для пользователя {request.user_id}: {e}"
        )
        raise HTTPException(status_code=500, detail="Ошибка при создании чата.")


@router.get("/get_chats")
async def get_chats(db: Database = Depends(get_db)):
    """
    Получение списка чатов. Можно передать ID пользователя, чтобы получить только его чаты.
    """
    try:
        # Получаем чаты для конкретного пользователя
        chats = await db.get_all_chats_with_last_message()
        if not chats:
            return {"status": "success", "message": "Чаты не найдены."}
        return {"status": "success", "data": chats}
    except Exception as e:
        logger.error(f"Ошибка при получении чатов: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при получении чатов.")


@router.get("/get_chat/{chat_id}")
async def get_chat(chat_id: int, db: Database = Depends(get_db)):
    """
    Получение одного чата по ID. Возвращает информацию о чате, если он существует.
    """
    try:
        # Получаем чат по ID
        chat = await db.get_chat_by_user_id(chat_id)
        if not chat:
            return {"status": "success", "message": "Чат не найден."}
        return {"status": "success", "data": chat}
    except Exception as e:
        logger.error(f"Ошибка при получении чата с ID {chat_id}: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при получении чата.")
