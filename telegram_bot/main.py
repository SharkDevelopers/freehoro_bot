from aiogram import Dispatcher
from loguru import logger

from telegram.middlewares import ObjectMiddleware
from utils import get_bot, get_media_manager, get_scheduler
from telegram.handlers import router


dp = Dispatcher()
bot = get_bot()
scheduler = get_scheduler()


# Создает кэш file_id фотографий
async def upload_media():
    await get_media_manager().upload_assets()


async def main():
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        dp.include_router(router)
        dp.message.outer_middleware(ObjectMiddleware())
        bot_info = await bot.get_me()
        await upload_media()
        scheduler.start()
        logger.info(f"Starting bot @{bot_info.username}[{bot_info.id}]")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as exc:
        logger.critical(exc)
    finally:
        logger.info("Stopping bot")
        await bot.session.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
