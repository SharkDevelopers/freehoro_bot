from flask import Blueprint

# Создаем блюпринт для авторизации
auth_blueprint = Blueprint(
    "auth", __name__, template_folder="templates", static_folder="static"
)

# Импортируем виды уже после создания блюпринта
from . import views
