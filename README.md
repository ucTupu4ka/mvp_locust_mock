# MVP: Locust + Mock API + Docker

Этот проект нужен как быстрый учебный и interview-ready MVP:
- поднять mock API в Docker;
- нагрузить API через Locust;
- получить базовые метрики (RPS, p95, error rate).

## Что мы сделали по шагам

### Шаг 1. Создали структуру проекта
Создали папки и файлы:
- `mock_api/` - сервис с API;
- `locust/` - нагрузочные сценарии;
- `docker-compose.yml` - поднимает оба сервиса;
- `.gitignore` - служебные исключения.

Зачем: чтобы сразу разделить ответственность между API и генератором нагрузки.

### Шаг 2. Реализовали mock API на FastAPI
Добавили 3 endpoint:
- `GET /health` - быстрая проверка доступности;
- `POST /orders` - создание заказа;
- `GET /orders/{id}` - чтение заказа.

Добавили негативное поведение:
- ~10% запросов на `POST /orders` возвращают `500`;
- ~20% запросов получают искусственную задержку.

Зачем: это имитирует "живой" нестабильный backend, а не стерильный mock.

### Шаг 3. Написали Locust-сценарии
Сделали пользователя `OrdersUser` с 3 задачами:
- health-check;
- create order;
- get order.

Логика:
- сохраняем `id` созданных заказов;
- читаем только реально созданные `id`;
- `500` на `POST` считаем ожидаемым поведением mock, а не падением теста.

Зачем: так сценарий ближе к реальному пользовательскому флоу.

### Шаг 4. Dockerize + Compose
Собрали два контейнера:
- `mock_api` (FastAPI + Uvicorn, порт `8000`);
- `locust` (Locust UI, порт `8089`).

Зачем: запуск проекта одной командой и воспроизводимость окружения.

### Шаг 5. Исправили технические проблемы
По ходу были ошибки:
- `docker compose` не работал (неполная установка окружения);
- `docker-compose.yml` был пустой;
- позже был дублирован блок `services`;
- в `app.py` и `locustfile.py` были дубли кода.

Все это исправлено, конфиг валиден (`docker-compose config` проходит).

---

## Как запустить

1) Убедиться, что Docker daemon запущен (Docker Desktop или Colima).  
2) В корне проекта выполнить:

```bash
docker-compose up --build
```

3) Открыть:
- Locust UI: `http://localhost:8089`
- API health: `http://localhost:8000/health`

---

## Как провести тест в Locust UI

Рекомендуемый базовый прогон:
- Number of users: `20`
- Spawn rate: `5`
- Время прогона: `2-3` минуты

Потом усиленный:
- Number of users: `50`
- Spawn rate: `10`

Что сохранить:
- скрин вкладки `Statistics`;
- `RPS`;
- `95%ile` (p95);
- `Failure %`.

---

## Аннотированные файлы (комментарий к каждой строке)

Ниже те же конфиги/код, но с пояснениями "строка -> что делает".

### `docker-compose.yml` (построчно)

```yaml
services: # объявляем сервисы compose-проекта
  mock_api: # имя сервиса mock API
    build: ./mock_api # собрать образ из папки mock_api
    container_name: mock_api # фиксированное имя контейнера
    ports: # проброс портов на хост
      - "8000:8000" # host:container для API

  locust: # имя сервиса с нагрузкой
    build: ./locust # собрать образ из папки locust
    container_name: locust # фиксированное имя контейнера
    ports: # проброс Locust UI
      - "8089:8089" # host:container для веб-интерфейса
    depends_on: # порядок старта сервисов
      - mock_api # сначала поднимется API
    command: > # команда запуска внутри контейнера
      locust -f /mnt/locust/locustfile.py --host http://mock_api:8000 # запуск Locust и target host
```

### `mock_api/Dockerfile` (построчно)

```dockerfile
FROM python:3.11-slim # базовый легкий Python-образ

WORKDIR /app # рабочая директория в контейнере
COPY requirements.txt . # копируем зависимости
RUN pip install --no-cache-dir -r requirements.txt # устанавливаем зависимости

COPY app.py . # копируем API-код
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"] # старт HTTP-сервера
```

### `mock_api/app.py` (построчно)

```python
import random # для вероятностного 500 и задержек
import time # для искусственной задержки
import uuid # для генерации id заказа

from fastapi import FastAPI, HTTPException # web framework и HTTP-исключения
from pydantic import BaseModel # валидация входного payload

app = FastAPI(title="Mock Orders API") # создаем приложение FastAPI
orders = {} # in-memory storage заказов


class OrderIn(BaseModel): # схема входящего запроса для POST /orders
    item: str # название товара
    qty: int # количество


@app.get("/health") # endpoint health-check
def health():
    return {"status": "ok"} # простой ответ, что сервис жив


@app.post("/orders") # endpoint создания заказа
def create_order(order: OrderIn):
    if random.random() < 0.1: # 10% запросов вернем 500
        raise HTTPException(status_code=500, detail="Random internal error") # симуляция ошибки сервера

    if random.random() < 0.2: # 20% запросов замедлим
        time.sleep(random.uniform(0.1, 0.5)) # задержка 100-500 мс

    order_id = str(uuid.uuid4()) # генерируем уникальный id
    orders[order_id] = {"id": order_id, "item": order.item, "qty": order.qty} # сохраняем заказ в память
    return orders[order_id] # возвращаем созданный заказ


@app.get("/orders/{order_id}") # endpoint чтения заказа по id
def get_order(order_id: str):
    if order_id not in orders: # если такого id нет
        raise HTTPException(status_code=404, detail="Order not found") # возвращаем 404
    return orders[order_id] # иначе отдаем заказ
```

### `locust/Dockerfile` (построчно)

```dockerfile
FROM python:3.11-slim # базовый Python-образ

WORKDIR /mnt/locust # рабочая директория для locust-файлов
COPY requirements.txt . # копируем список зависимостей
RUN pip install --no-cache-dir -r requirements.txt # устанавливаем locust

COPY locustfile.py . # копируем сценарий нагрузки
```

### `locust/locustfile.py` (построчно)

```python
import random # случайный выбор payload и id

from locust import HttpUser, between, task # базовые сущности Locust


class OrdersUser(HttpUser): # модель виртуального пользователя
    wait_time = between(0.2, 1.0) # пауза между запросами 200-1000 мс
    created_order_ids = [] # список id созданных заказов для GET

    @task(2) # вес задачи: health будет реже, чем create_order
    def health_check(self):
        self.client.get("/health", name="/health") # GET /health

    @task(5) # основная нагрузка на создание заказов
    def create_order(self):
        payload = { # тело POST-запроса
            "item": random.choice(["book", "pen", "notebook", "mouse"]), # случайный товар
            "qty": random.randint(1, 5), # случайное количество
        }

        with self.client.post( # отправляем POST /orders
            "/orders", json=payload, name="/orders [POST]", catch_response=True # даем вручную пометить успех/ошибку
        ) as resp:
            if resp.status_code == 200: # успешное создание
                data = resp.json() # читаем JSON-ответ
                order_id = data.get("id") # достаем id
                if order_id: # если id есть
                    self.created_order_ids.append(order_id) # добавляем в список для будущего GET
                resp.success() # считаем запрос успешным
            elif resp.status_code == 500: # ожидаемый негативный ответ mock API
                resp.success() # не считаем падением теста
            else:
                resp.failure(f"Unexpected status: {resp.status_code}") # любой другой код считаем ошибкой

    @task(3) # GET-задача средняя по частоте
    def get_order(self):
        if not self.created_order_ids: # если еще нет созданных заказов
            return # пропускаем шаг
        order_id = random.choice(self.created_order_ids) # выбираем случайный id из созданных
        with self.client.get( # отправляем GET /orders/{id}
            f"/orders/{order_id}", name="/orders/{id} [GET]", catch_response=True # именуем запрос для статистики
        ) as resp:
            if resp.status_code == 200: # ожидаем 200
                resp.success() # успех
            else:
                resp.failure(f"Unexpected status: {resp.status_code}") # иначе ошибка
```

---

## Полезные команды с пояснениями

```bash
docker-compose config # проверить, что compose-файл валиден
docker-compose up --build # собрать образы и поднять сервисы
docker-compose ps # посмотреть состояние контейнеров
docker-compose logs -f mock_api # смотреть логи API в реальном времени
docker-compose logs -f locust # смотреть логи Locust
docker-compose down # остановить и удалить контейнеры
```

---

## Короткое объяснение для интервью

"Я сделал Dockerized MVP: mock API + Locust. Смоделировал базовые endpoint и нестабильность (random 500 + delay), затем снял p95/error rate/RPS. Это показало, что я могу быстро поднять новый инструмент и применить его на практике."
