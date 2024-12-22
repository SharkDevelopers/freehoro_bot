import os
from functools import lru_cache
from aiogram import Bot
from aiogram_media_cache import MediaManager
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from shared.storage import Database
from conf import config

project_root = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(project_root, "data")
os.makedirs(data_path, exist_ok=True)

db_path = f"sqlite:///{os.path.join(data_path, 'jobs.db')}"


@lru_cache()
def get_bot() -> Bot:
    return Bot(config.bot_token)


@lru_cache()
def get_db() -> Database:
    return Database(config.db_name, uri=config.mongo_uri, logger=logger)


@lru_cache
def get_media_manager() -> MediaManager:
    return MediaManager(
        bot=get_bot(),
        upload_id=config.upload_chat_id,
        assets_dir="data/assets/",
        cache_file="data/file_ids.plk",
    )


@lru_cache
def get_scheduler() -> AsyncIOScheduler:
    return AsyncIOScheduler(jobstores={"default": SQLAlchemyJobStore(url=db_path)})
