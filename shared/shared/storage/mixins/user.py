from logging import Logger
from typing import Any, Optional

from ..models import User


class UserMixin:
    users: Any
    logger: Logger

    async def create_user(self, user: User) -> Optional[User]:
        """Создание нового пользователя."""
        try:
            # Преобразуем данные пользователя в словарь и сохраняем в базу данных
            user_dict = user.to_dict()  # Преобразуем в словарь с учетом поля sendings
            await self.users.insert_one(user_dict)
            self.logger.info(f"Пользователь с id {user.id} успешно создан.")
            return user
        except Exception as e:
            self.logger.error(f"Ошибка при создании пользователя: {e}")
            return None

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Получение пользователя по его ID."""
        try:
            data = await self.users.find_one({"id": user_id})
            if data:
                self.logger.info(f"Пользователь с id {user_id} найден.")
                print("data:", data)
                return User(**data)  # Восстанавливаем объект User из словаря
            self.logger.warning(f"Пользователь с id {user_id} не найден.")
            return None
        except Exception as e:
            self.logger.error(f"Ошибка при получении пользователя с id {user_id}: {e}")
            return None

    async def update_user(self, user_id: int, update_data: dict) -> bool:
        """Обновление данных пользователя."""
        try:
            # Обновляем только необходимые данные, включая поле sendings, если оно указано
            result = await self.users.update_one(
                {"id": user_id},
                {"$set": update_data},  # Обновляем только те поля, которые переданы
            )
            if result.modified_count > 0:
                self.logger.info(f"Пользователь с id {user_id} успешно обновлен.")
                return True
            self.logger.warning(f"Пользователь с id {user_id} не был обновлен.")
            return False
        except Exception as e:
            self.logger.error(f"Ошибка при обновлении пользователя с id {user_id}: {e}")
            return False

    async def delete_user(self, user_id: int) -> bool:
        """Удаление пользователя по его ID."""
        try:
            result = await self.users.delete_one({"id": user_id})
            if result.deleted_count > 0:
                self.logger.info(f"Пользователь с id {user_id} успешно удален.")
                return True
            self.logger.warning(f"Пользователь с id {user_id} не найден для удаления.")
            return False
        except Exception as e:
            self.logger.error(f"Ошибка при удалении пользователя с id {user_id}: {e}")
            return False
