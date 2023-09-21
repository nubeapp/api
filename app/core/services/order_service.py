from typing import List
from sqlalchemy.orm import Session

from app.core.repositories.order_repository import OrderRepository
from app.api.models.order import OrderResponse
from app.schemas.order import Order

class OrderService:
    @staticmethod
    async def get_orders_by_user_id(db: Session, user_id: int) -> List[OrderResponse]:
        orders = await OrderRepository.get_orders_by_user_id(db, user_id)
        return orders

    @staticmethod
    async def create_order(db: Session, user_id: int) -> Order:
        new_order = await OrderRepository.create_order(db, user_id)
        return new_order
