FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем pyproject.toml и poetry.lock
COPY pyproject.toml /app
# Устанавливаем зависимости через poetry
RUN pip install poetry
RUN poetry install

# Копируем весь проект
COPY . /app/
