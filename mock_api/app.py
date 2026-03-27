import random # Случайность для имитации ошибок и задержек.
import time # Используется для искусственной задержки.
import uuid # Используется для генерации уникальных id заказов.

from fastapi import FastAPI, HTTPException # Приложение FastAPI и helper для HTTP-ошибок.
from pydantic import BaseModel # Pydantic-модели для валидации входных данных.

app = FastAPI(title="Mock Orders API") # Создаём инстанс FastAPI приложения.
orders = {} # In-memory хранилище заказов (очищается при перезапуске контейнера).


class OrderIn(BaseModel): # Схема тела запроса для `POST /orders`.
    item: str # Поле `item` (строка).
    qty: int # Поле `qty` (целое число).


@app.get("/health") # Эндпоинт проверки доступности.
def health(): # Обработчик `GET /health`.
    return {"status": "ok"} # Возвращаем простой ответ о доступности.


@app.post("/orders") # Эндпоинт создания заказа.
def create_order(order: OrderIn): # Обработчик `POST /orders` (тело валидируется Pydantic).
    if random.random() < 0.1: # Имитируем примерно 10% случайных ошибок сервера.
        raise HTTPException( # Генерируем HTTP 500, чтобы Locust учитывал это как ошибку.
            status_code=500, detail="Random internal error" # Статус 500 и текст ошибки.
        ) # Завершаем генерацию HTTPException.

    if random.random() < 0.2: # Имитируем примерно 20% шанс искусственной задержки.
        time.sleep( # Блокируем обработчик, как будто зависимость отвечает медленно.
            random.uniform(0.1, 0.5) # Задержка между 0.1 и 0.5 секунды.
        ) # Завершаем sleep.

    order_id = str(uuid.uuid4()) # Генерируем уникальный id заказа.
    orders[order_id] = {  # Сохраняем заказ в памяти, чтобы потом уметь его прочитать.
        "id": order_id, "item": order.item, "qty": order.qty
    } # Завершаем создание словаря заказа.
    return orders[order_id] # Возвращаем созданный заказ.


@app.get("/orders/{order_id}") # Эндпоинт чтения заказа по id.
def get_order(order_id: str): # Обработчик `GET /orders/{order_id}`.
    if order_id not in orders: # Если такого заказа нет в памяти.
        raise HTTPException( # Возвращаем 404, если заказ отсутствует.
            status_code=404, detail="Order not found" # Статус 404 и текст ошибки.
        ) # Завершаем генерацию HTTPException.
    return orders[order_id] # Возвращаем сохраненный заказ.