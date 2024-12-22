from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.base import timedelta
from apscheduler.triggers.date import DateTrigger
from aiogram import Bot
from aiogram_media_cache import MediaManager
from loguru import logger

from shared.storage import Database
from utils import get_bot, get_db, get_media_manager, get_scheduler
from . import constants

bot: Bot = get_bot()
db: Database = get_db()
media_manager: MediaManager = get_media_manager()
scheduler: AsyncIOScheduler = get_scheduler()

# TODO: заменить sqlite на mongodb
# TODO: связать логику планирования с сущность User(metadata.sendings)


def planing_push(chat_id: int, push_num: int):
    """Планирование следующего пуша с сохранением."""
    if push_num < len(constants.text_hours_sending):
        delay = constants.text_hours_sending[push_num]["sleep"]
        scheduler.add_job(
            send_push,
            trigger=DateTrigger(run_date=datetime.now() + timedelta(seconds=delay)),
            args=[chat_id, push_num],
            id=f"push_{chat_id}_{push_num}",
            replace_existing=True,
            misfire_grace_time=None,
        )


async def send_push(chat_id, push_num: int):
    """Отправка запланированного пуша."""
    try:
        user = await db.get_user_by_id(chat_id)
        if not user:
            logger.warning(f"Пользователь с ID {chat_id} не найден.")
            return

        data = constants.text_hours_sending[push_num]
        sendings = user.metadata.get("sendings", {})
        if not sendings.get(data["name"]):
            await bot.send_photo(
                user.id,
                photo=media_manager.get_file_id(data["photo"]),
                caption=data["text"],
                parse_mode="HTML",
            )
            user.metadata["sendings"][data["name"]] = "Отправлено"
            await db.update_user(user.id, {"metadata": user.metadata})
            logger.info(f"Пуш {data['name']} успешно отправлен.")
    except Exception as e:
        logger.error(f"Ошибка при отправке пуша {push_num}: {e}")
    finally:
        planing_push(chat_id, push_num + 1)
