import os
from flask import render_template, redirect, url_for, request, flash, session
from . import auth_blueprint
from .forms import LoginForm
from .utils import check_credentials
import requests
from dotenv import load_dotenv

load_dotenv()
# Статичный логин и пароль
USER_CREDENTIALS = {
    "username": os.getenv("username_app"),
    "password": os.getenv("password_app"),
}

from flask import jsonify


@auth_blueprint.route("/api/chats/<int:user_id>/send_message", methods=["POST"])
def send_message(user_id):
    """Отправка сообщения в чат"""
    try:
        # Получение текста сообщения из POST-запроса
        message_text = request.form.get("text", "").strip()

        # Проверка: сообщение не должно быть пустым
        if not message_text:
            return (
                jsonify({"status": "error", "message": "Message cannot be empty."}),
                400,
            )

        # Отправка сообщения во внешний сервис
        url = "http://localhost:8005/send_message"
        payload = {"user_id": int(user_id), "text": str(message_text)}
        headers = {"Content-Type": "application/json"}
        print(payload)
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()  # Проверяем статус-код ответа
        except requests.exceptions.RequestException as e:
            # Логирование ошибок внешнего запроса
            return (
                jsonify({"status": "error", "message": f"External service error: {e}"}),
                500,
            )

        return (
            jsonify({"status": "success", "message": "Message sent successfully."}),
            200,
        )

    except Exception as e:
        # Общий обработчик исключений
        return jsonify({"status": "error", "message": str(e)}), 500


@auth_blueprint.route("/api/chats/<int:user_id>", methods=["GET"])
def get_chat_messages(user_id):
    # Отправляем запрос к внешнему API
    response = requests.get(f"http://localhost:8005/get_chat/{user_id}")
    response.raise_for_status()  # Если статус-код не 200, будет выброшено исключение

    print(response.json())
    chat = response.json().get("data", [])
    if chat:
        return jsonify(chat)
    else:
        return jsonify({"status": "error", "message": "Chat not found"}), 404


@auth_blueprint.route("/api/chats", methods=["GET"])
def get_chats():
    """API для получения списка чатов"""

    try:
        # Отправляем запрос к внешнему API
        response = requests.get("http://localhost:8005/get_chats")
        response.raise_for_status()  # Если статус-код не 200, будет выброшено исключение

        chats = response.json().get("chats", [])
        # Фильтрация по ключевым словам в последнем сообщении
        filter_text = request.args.get(
            "filter", ""
        )  # Получаем фильтр из параметров запроса
        if filter_text:
            chats = [
                chat
                for chat in chats
                if filter_text.lower() in chat["messages"][0]["text"].lower()
            ]

        # Сортировка чатов по дате последнего сообщения
        chats.sort(key=lambda x: x["messages"][0]["created_at"], reverse=True)
        # Возвращаем чаты в формате JSON
        return jsonify({"status": "success", "data": chats})

    except requests.exceptions.RequestException as e:
        # Обрабатываем ошибки запроса
        return jsonify({"error": f"Ошибка при получении чатов: {str(e)}"}), 500


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Проверяем введенные данные
        if check_credentials(username, password, USER_CREDENTIALS):
            session["username"] = username
            flash("Login successful!", "success")
            return redirect(url_for("auth.dashboard"))
        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html", form=form)


@auth_blueprint.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("auth.login"))

    return render_template("dashboard.html", username=session["username"])


@auth_blueprint.route("/logout")
def logout():
    session.pop("username", None)
    flash("You have been logged out!", "info")
    return redirect(url_for("auth.login"))
