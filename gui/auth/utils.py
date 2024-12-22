# auth/utils.py


def check_credentials(username, password, user_credentials):
    """
    Функция для проверки введенных учетных данных (логин и пароль)
    с заранее заданными значениями.

    :param username: введенный логин
    :param password: введенный пароль
    :param user_credentials: словарь с правильными учетными данными
    :return: True, если учетные данные совпадают, иначе False
    """
    return (
        user_credentials.get("username") == username
        and user_credentials.get("password") == password
    )


def hash_password(password):
    """
    Пример функции для хеширования пароля.
    На практике используйте более безопасные алгоритмы, например, bcrypt.
    """
    import hashlib

    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(stored_hash, password):
    """
    Проверка пароля с хешем.
    """
    return stored_hash == hash_password(password)
