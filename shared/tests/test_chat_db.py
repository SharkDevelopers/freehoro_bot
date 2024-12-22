import pytest
from shared.storage.models import Chat, Message, MessageType, User
from shared.storage.models.message import DirectionType


@pytest.mark.anyio
async def test_create_chat(mock_db):
    """Тестируем создание чата"""
    user = User(id=1, full_name="Test User", username="testuser")
    chat = Chat(user_id=user.id, full_name=user.full_name, username=user.username)

    # Создаем чат
    created_chat = await mock_db.create_chat(chat)
    assert created_chat is not None
    assert created_chat.user_id == 1
    assert created_chat.username == "testuser"


@pytest.mark.anyio
async def test_get_chat_by_user_id(mock_db):
    """Тестируем получение чата по user_id"""
    user = User(id=1, full_name="Test User", username="testuser")
    chat = Chat(user_id=user.id, full_name=user.full_name, username=user.username)

    # Создаем чат
    await mock_db.create_chat(chat)

    # Получаем чат по user_id
    retrieved_chat = await mock_db.get_chat_by_user_id(user.id)
    assert retrieved_chat is not None
    assert retrieved_chat.user_id == 1
    assert retrieved_chat.username == "testuser"


@pytest.mark.anyio
async def test_add_message_to_chat(mock_db):
    """Тестируем добавление сообщения в чат"""
    user = User(id=1, full_name="Test User", username="testuser")
    chat = Chat(user_id=user.id, full_name=user.full_name, username=user.username)
    message = Message(
        id=1,
        direction=DirectionType.incoming,
        type=MessageType.text,
        text="Test message",
    )

    # Создаем чат
    chat = await mock_db.create_chat(chat)
    # Добавляем сообщение в чат
    added = await mock_db.add_message_to_chat(user.id, message)
    assert added is True

    # Получаем чат и проверяем количество сообщений
    updated_chat = await mock_db.get_chat_by_user_id(user.id)
    assert len(updated_chat.messages) == 1
    assert updated_chat.messages[0].text == "Test message"


@pytest.mark.anyio
async def test_clear_chat_messages(mock_db):
    """Тестируем очистку сообщений в чате"""
    user = User(id=1, full_name="Test User", username="testuser")
    chat = Chat(user_id=user.id, full_name=user.full_name, username=user.username)
    message = Message(
        id=1,
        direction=DirectionType.incoming,
        type=MessageType.text,
        text="Test message",
    )

    # Создаем чат и добавляем сообщение
    await mock_db.create_chat(chat)
    await mock_db.add_message_to_chat(user.id, message)

    # Очистка сообщений в чате
    cleared = await mock_db.clear_chat_messages(user.id)
    assert cleared is True

    # Получаем чат и проверяем, что сообщения очищены
    updated_chat = await mock_db.get_chat_by_user_id(user.id)
    assert len(updated_chat.messages) == 0


@pytest.mark.anyio
async def test_get_all_chats_with_last_message(mock_db):
    """Тестируем получение всех чатов с последним сообщением"""
    user1 = User(id=1, full_name="Test User 1", username="testuser1")
    user2 = User(id=2, full_name="Test User 2", username="testuser2")

    chat1 = Chat(user_id=user1.id, full_name=user1.full_name, username=user1.username)
    chat2 = Chat(user_id=user2.id, full_name=user2.full_name, username=user2.username)

    message1 = Message(
        id=1,
        direction=DirectionType.incoming,
        type=MessageType.text,
        text="Test message 1",
    )
    message2 = Message(
        id=2,
        direction=DirectionType.incoming,
        type=MessageType.text,
        text="Test message 2",
    )

    # Создаем чаты и добавляем сообщения
    await mock_db.create_chat(chat1)
    await mock_db.create_chat(chat2)
    await mock_db.add_message_to_chat(user1.id, message1)
    await mock_db.add_message_to_chat(user2.id, message2)

    # Получаем все чаты и последние сообщения
    chats = await mock_db.get_all_chats_with_last_message()

    assert chats[0]["user_id"] == user1.id
    assert chats[1]["user_id"] == user2.id
    assert chats[0]["last_message"]["text"] == "Test message 1"
    assert chats[1]["last_message"]["text"] == "Test message 2"
