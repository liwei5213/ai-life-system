from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol
from urllib.parse import quote

from core.pay.order_manager import Order, OrderManager, order_manager


class PayProvider(Protocol):
    def create_payment(self, order: Order, return_url: str | None = None) -> str:
        ...

    def verify_payment(self, order_id: str) -> bool:
        ...

    def handle_callback(self, payload: dict[str, str]) -> bool:
        ...


@dataclass
class WeChatPayConfig:
    appid: str = ""
    mchid: str = ""
    api_v3_key: str = ""
    notify_url: str = ""


class WeChatPayProvider:
    def __init__(
        self,
        order_manager: OrderManager,
        config: WeChatPayConfig | None = None,
        base_url: str = "http://127.0.0.1:8000",
    ) -> None:
        self.order_manager = order_manager
        self.config = config or WeChatPayConfig()
        self.base_url = base_url.rstrip("/")

    def create_payment(self, order: Order, return_url: str | None = None) -> str:
        self.order_manager.update_status(order.order_id, "pending")
        pay_url = f"{self.base_url}/pay/h5?order_id={order.order_id}"
        if return_url:
            pay_url += f"&return_url={quote(return_url, safe='')}"
        return pay_url

    def verify_payment(self, order_id: str) -> bool:
        order = self.order_manager.update_status(order_id, "paid")
        return order is not None

    def handle_callback(self, payload: dict[str, str]) -> bool:
        order_id = payload.get("order_id", "")
        if not order_id:
            return False
        return self.verify_payment(order_id)


wechat_pay_provider: PayProvider = WeChatPayProvider(order_manager=order_manager)
