import pytest
from mongomock_motor import AsyncMongoMockClient
from shared.storage import Database


@pytest.fixture(scope="function")
async def mock_db():
    """Мокируем MongoDB для тестов."""
    db = Database(client=AsyncMongoMockClient(), db_name="test_db")  # type: ignore
    yield db
    # Получаем список коллекций асинхронно
    collections = await db.db.list_collection_names()  # Используем await
    for collection in collections:
        await db.db[collection].drop()  # Удаляем коллекции асинхронно
    db.disconnect()  # Закрытие соединения с базой данных асинхронно
