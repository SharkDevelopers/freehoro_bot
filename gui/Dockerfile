FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /gui

# Копируем зависимости (если есть requirements.txt)
COPY req.txt /gui/

# Устанавливаем зависимости с помощью pip
RUN pip install -r req.txt

# Копируем весь проект
COPY . /gui/
