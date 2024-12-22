import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Секретный ключ для сессий
app.secret_key = os.getenv("secret_key_app")
print(os.getenv("secret_key_app"))
# Регистрация блюпринта для авторизации
from auth import auth_blueprint

app.register_blueprint(auth_blueprint)
if __name__ == "__main__":
    app.run(host="localhost", port=int(os.getenv("flask_port")), debug=True)
