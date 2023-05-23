from typing import List

from ..models import OrderResponse
from .. import schemas
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi import Depends, APIRouter
from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/orders",
    tags=['Orders']
)

@router.get("", response_model=List[OrderResponse])
async def get_orders_by_user_id(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    orders = db.query(schemas.Order).filter(schemas.Order.user_id == current_user.id).all()
    for order in orders:
        order.tickets = db.query(schemas.Ticket).filter(schemas.Ticket.order_id == order.id).all()
    return orders

async def create_order(user_id: int,db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    new_order = schemas.Order(user_id=user_id)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order