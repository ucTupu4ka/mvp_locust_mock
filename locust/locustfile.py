import random

from locust import HttpUser, between, task


class OrdersUser(HttpUser):
    wait_time = between(0.2, 1.0)
    created_order_ids = []

    @task(2)
    def health_check(self):
        self.client.get("/health", name="/health")

    @task(5)
    def create_order(self):
        payload = {
            "item": random.choice(["book", "pen", "notebook", "mouse"]),
            "qty": random.randint(1, 5),
        }

        with self.client.post(
            "/orders", json=payload, name="/orders [POST]", catch_response=True
        ) as resp:
            if resp.status_code == 200:
                data = resp.json()
                order_id = data.get("id")
                if order_id:
                    self.created_order_ids.append(order_id)
                resp.success()
            elif resp.status_code == 500:
                resp.success()
            else:
                resp.failure(f"Unexpected status: {resp.status_code}")

    @task(3)
    def get_order(self):
        if not self.created_order_ids:
            return
        order_id = random.choice(self.created_order_ids)
        with self.client.get(
            f"/orders/{order_id}", name="/orders/{id} [GET]", catch_response=True
        ) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"Unexpected status: {resp.status_code}")