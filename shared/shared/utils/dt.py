import pytz
from typing import Optional, Union
from datetime import datetime


class TimeUtils:
    """
    Утилитарный класс для работы с датой и временем в часовом поясе МСК.
    """

    def __init__(self, datetime_value: Optional[Union[str, datetime]] = None):
        """
        Инициализация класса.
        Если datetime_value не передан, используется текущее время в МСК.
        Если передано строковое представление времени, преобразуется в datetime.
        Если передан datetime, конвертируется в МСК.
        """
        self.timezone = pytz.timezone("Europe/Moscow")

        if isinstance(datetime_value, str):
            # Если передана строка, пробуем преобразовать её в datetime
            self.value = self._convert_str_to_datetime(datetime_value)
        elif isinstance(datetime_value, datetime):
            # Если передан datetime, конвертируем его в МСК
            self.value = self._convert_to_msk_timezone(datetime_value)
        else:
            # Если не передано, берем текущее время
            self.value = datetime.now(self.timezone)

    def _convert_to_msk_timezone(self, dt: datetime) -> datetime:
        """
        Преобразует переданное время в часовую зону МСК.
        """
        if dt.tzinfo is None:
            # Если объект datetime без часового пояса, добавляем часовой пояс МСК
            return self.timezone.localize(dt)
        else:
            # Если у datetime уже есть часовой пояс, конвертируем его в МСК
            return dt.astimezone(self.timezone)

    def _convert_str_to_datetime(self, date_str: str) -> datetime:
        """
        Преобразует строку в datetime в формате "%Y:%m:%d %H:%M:%S".
        """
        try:
            return datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
        except ValueError:
            raise ValueError(
                f"Строка '{date_str}' не соответствует формату '%Y:%m:%d %H:%M:%S'"
            )

    def __str__(self):
        """
        Возвращает строковое представление текущего времени в формате "%Y:%m:%d %H:%M:%S".
        """
        return self.value.strftime("%Y:%m:%d %H:%M:%S")

    @classmethod
    def from_datetime(cls, datetime_value: datetime) -> "TimeUtils":
        """
        Создает объект TimeUtils из переданного datetime.
        """
        return cls(datetime_value)

    @classmethod
    def from_string(cls, date_str: str) -> "TimeUtils":
        """
        Создает объект TimeUtils из строки в формате "%Y:%m:%d %H:%M:%S".
        """
        return cls(datetime_value=date_str)
