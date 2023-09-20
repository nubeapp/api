# core/repositories/order_repository.py

from typing import List
from sqlalchemy.orm import Session

from app.models.order import OrderResponse
from app.schemas.order import Order
from app.schemas.ticket import Ticket
from app.schemas.event import Event



class OrderRepository:
    @staticmethod
    async def get_orders_by_user_id(db: Session, user_id: int) -> List[OrderResponse]:
        orders = (
            db.query(Order)
            .filter(Order.user_id == user_id)
            .all()
        )

        for order in orders:
            tickets = db.query(Ticket).filter(Ticket.order_id == order.id).all()
            order.event = db.query(Event).filter(Event.id == tickets[0].event_id).first()
            order.tickets = tickets

        return orders

    @staticmethod
    async def create_order(db: Session, user_id: int) -> Order:
        new_order = Order(user_id=user_id)
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        return new_order
