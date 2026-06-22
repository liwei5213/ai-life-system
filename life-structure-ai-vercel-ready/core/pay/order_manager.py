from __future__ import annotations

from dataclasses import asdict, dataclass
from time import time
from typing import Literal
from uuid import uuid4

OrderStatus = Literal["created", "pending", "paid"]
PayType = Literal["wechat"]


@dataclass
class Order:
    order_id: str
    amount: int
    status: OrderStatus
    pay_type: PayType
    created_at: float

    def to_dict(self) -> dict[str, str | int | float]:
        return asdict(self)


class OrderManager:
    def __init__(self) -> None:
        self._orders: dict[str, Order] = {}

    def create_order(self, amount: int = 29, pay_type: PayType = "wechat") -> Order:
        order = Order(
            order_id=uuid4().hex,
            amount=amount,
            status="created",
            pay_type=pay_type,
            created_at=time(),
        )
        self._orders[order.order_id] = order
        return order

    def get_order(self, order_id: str) -> Order | None:
        return self._orders.get(order_id)

    def update_status(self, order_id: str, status: OrderStatus) -> Order | None:
        order = self.get_order(order_id)
        if order is None:
            return None

        order.status = status
        return order

    def is_paid(self, order_id: str) -> bool:
        order = self.get_order(order_id)
        return order is not None and order.status == "paid"


order_manager = OrderManager()
