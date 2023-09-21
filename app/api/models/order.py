from datetime import datetime
from pydantic import BaseModel

from app.api.models.ticket import TicketSummary

class OrderBase(BaseModel):
    pass

class OrderRequest(OrderBase):
    event_id: int
    quantity: int

class OrderResponse(TicketSummary):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
