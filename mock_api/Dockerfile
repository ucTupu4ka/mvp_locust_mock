FROM python:3.11-slim # Базовый легкий образ Python (меньше, чем полноценные Debian-образы).

WORKDIR /app # Рабочая директория внутри контейнера.
COPY requirements.txt . # Копируем список зависимостей в образ.
RUN pip install --no-cache-dir -r requirements.txt # Устанавливаем зависимости без кеша.

COPY app.py . # Копируем код FastAPI приложения в образ.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"] # Запускаем API-сервер и привязываемся ко всем интерфейсам.
