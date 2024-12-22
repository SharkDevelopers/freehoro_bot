import os

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict

# Путь к директории для логов
log_directory = "data/logs"

# Создаем директорию для логов, если она не существует
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

logger.add(
    os.path.join(log_directory, "log_{time:YYYY-MM-DD}.log"),
    rotation="3 days",  # Архивируем каждые 3 дня
    retention="30 days",  # Сохраняем логи не более 30 дней
    compression="zip",  # Архивируем старые логи в формате zip
    level="INFO",  # Уровень логирования
    encoding="utf-8",  # Кодировка файлов
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",  # Формат записи
)


class Config(BaseSettings):
    mongo_uri: str
    db_name: str
    bot_token: str
    app_port: int
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


config = Config()  # type: ignore
