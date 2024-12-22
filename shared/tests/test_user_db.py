import pytest
from shared.storage.models import User
from datetime import datetime

from shared.utils.dt import TimeUtils


@pytest.mark.anyio
async def test_create_user(mock_db):
    """Тестируем создание пользователя"""
    user = User(
        id=1,
        full_name="Test User",
        username="testuser",
        created_at=datetime.now(),
    )

    # Создаем пользователя
    created_user = await mock_db.create_user(user)
    assert created_user is not None
    assert created_user.id == 1
    assert created_user.full_name == "Test User"
    assert created_user.username == "testuser"


@pytest.mark.anyio
async def test_get_user_by_id(mock_db):
    """Тестируем получение пользователя по user_id"""
    user = User(
        id=1,
        full_name="Test User",
        username="testuser",
        created_at=datetime.now(),
    )
    print(user.to_dict())
    # Создаем пользователя
    assert await mock_db.create_user(user) is not None

    # Получаем пользователя по user_id
    retrieved_user = await mock_db.get_user_by_id(user.id)
    assert retrieved_user is not None
    assert retrieved_user.id == 1
    assert retrieved_user.full_name == "Test User"
    assert retrieved_user.username == "testuser"


@pytest.mark.anyio
async def test_update_user(mock_db):
    """Тестируем обновление данных пользователя"""
    user = User(
        id=1, full_name="Test User", username="testuser", created_at=datetime.now()
    )

    # Создаем пользователя
    await mock_db.create_user(user)

    # Обновляем пользователя
    update_data = {"full_name": "Updated User"}
    update_result = await mock_db.update_user(user.id, update_data)
    assert update_result is True

    # Проверяем, что данные обновились
    updated_user = await mock_db.get_user_by_id(user.id)
    assert updated_user.full_name == "Updated User"


@pytest.mark.anyio
async def test_delete_user(mock_db):
    """Тестируем удаление пользователя"""
    user = User(
        id=1, full_name="Test User", username="testuser", created_at=datetime.now()
    )

    # Создаем пользователя
    await mock_db.create_user(user)

    # Удаляем пользователя
    delete_result = await mock_db.delete_user(user.id)
    assert delete_result is True

    # Проверяем, что пользователь был удален
    deleted_user = await mock_db.get_user_by_id(user.id)
    assert deleted_user is None


@pytest.mark.anyio
async def test_user_not_found(mock_db):
    """Тестируем ситуацию, когда пользователь не найден"""
    user = await mock_db.get_user_by_id(999)  # Пользователь с таким ID не существует
    assert user is None
