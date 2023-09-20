# api/endpoints/order_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.services.order_service import OrderService
from app.database import get_db
from app.oauth2 import get_current_user
from typing import List
from app.models.order import OrderResponse

router = APIRouter(
    prefix="/orders",
    tags=['Orders']
)

@router.get("", response_model=List[OrderResponse])
async def get_orders_by_user_id(
    db: Session = Depends(get_db), current_user: int = Depends(get_current_user)
):
    orders = await OrderService.get_orders_by_user_id(db, current_user.id)
    return orders

@router.post("", response_model=OrderResponse)
async def create_order(
    db: Session = Depends(get_db), current_user: int = Depends(get_current_user)
):
    new_order = await OrderService.create_order(db, current_user.id)
    return new_order
