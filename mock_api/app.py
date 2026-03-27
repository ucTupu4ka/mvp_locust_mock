import random
import time
import uuid

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Mock Orders API")
orders = {}


class OrderIn(BaseModel):
    item: str
    qty: int


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/orders")
def create_order(order: OrderIn):
    if random.random() < 0.1:
        raise HTTPException(status_code=500, detail="Random internal error")

    if random.random() < 0.2:
        time.sleep(random.uniform(0.1, 0.5))

    order_id = str(uuid.uuid4())
    orders[order_id] = {"id": order_id, "item": order.item, "qty": order.qty}
    return orders[order_id]


@app.get("/orders/{order_id}")
def get_order(order_id: str):
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders[order_id]