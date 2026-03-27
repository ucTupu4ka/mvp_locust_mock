FROM python:3.11-slim # Базовый образ Python для запуска Locust в контейнере.

WORKDIR /mnt/locust # Рабочая директория, где лежит locustfile.
COPY requirements.txt . # Копируем список зависимостей для Locust в образ.
RUN pip install --no-cache-dir -r requirements.txt # Устанавливаем зависимости без кеша.

COPY locustfile.py . # Копируем сценарий Locust в образ.
