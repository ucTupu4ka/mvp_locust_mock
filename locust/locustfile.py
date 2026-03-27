import random # Используется для вариативного payload и выбора id ранее созданных заказов.

from locust import HttpUser, between, task # Основные классы/декораторы/хелперы Locust.


class OrdersUser(HttpUser): # Модель поведения пользователя в нагрузочном тесте.
    wait_time = between(0.2, 1.0) # Случайная пауза между задачами (0.2-1.0 сек).
    created_order_ids = [] # Список id созданных заказов для последующих запросов `GET`.

    @task(2) # Относительный вес: `health_check` выполняется реже, чем `create_order`.
    def health_check(self): # Задача для запроса `GET /health`.
        self.client.get("/health", name="/health") # Выполняем запрос и подписываем для статистики.

    @task(5) # Больший вес => задача выполняется чаще.
    def create_order(self): # Задача для `POST /orders`.
        payload = { # Формируем JSON-данные для тела запроса.
            "item": random.choice(["book", "pen", "notebook", "mouse"]), # Случайный выбор товара.
            "qty": random.randint(1, 5), # Случайная величина количества.
        } # Завершаем сбор payload.

        with self.client.post( # Отправляем `POST /orders` и перехватываем ответ для кастомной логики success/failure.
            "/orders", json=payload, name="/orders [POST]", catch_response=True # Детали запроса и режим catch_response.
        ) as resp: # resp позволяет проверить `status_code` и тело ответа.
            if resp.status_code == 200: # Успешный сценарий: mock вернул созданный заказ.
                data = resp.json() # Парсим JSON-ответ.
                order_id = data.get("id") # Достаём id заказа.
                if order_id: # Сохраняем только если id реально присутствует.
                    self.created_order_ids.append(order_id) # Запоминаем id для последующего GET.
                resp.success() # Помечаем запрос как успешный.
            elif resp.status_code == 500: # Негативный сценарий: mock сгенерировал внутреннюю ошибку.
                resp.success() # Для MVP считаем 500 ожидаемым вариантом.
            else: # Любой другой статус считаем неожиданным.
                resp.failure(f"Unexpected status: {resp.status_code}") # Помечаем как failure с причиной.

    @task(3) # Задача выполняется между частотами `health_check` и `create_order`.
    def get_order(self): # Задача для `GET /orders/{order_id}`.
        if not self.created_order_ids: # Если ещё нет созданных заказов.
            return # Пропускаем до тех пор, пока `create_order` не создаст хотя бы один id.
        order_id = random.choice(self.created_order_ids) # Выбираем id ранее созданного заказа.
        with self.client.get( # Отправляем `GET` для выбранного id.
            f"/orders/{order_id}", name="/orders/{id} [GET]", catch_response=True # URL и подпись для статистики.
        ) as resp: # resp позволяет проверить status_code.
            if resp.status_code == 200: # Ожидаем, что заказ найден и возвращён.
                resp.success() # Помечаем как успешный запрос.
            else: # Неожиданное состояние (например, 404).
                resp.failure(f"Unexpected status: {resp.status_code}") # Помечаем как failure для видимости.