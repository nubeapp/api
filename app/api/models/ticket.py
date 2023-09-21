from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from typing import List
from enum import Enum
from app.api.models.event import EventResponse

from app.api.models.user import UserResponse

class TicketStatus(Enum):
    AVAILABLE = 'AVAILABLE'
    SOLD = 'SOLD'
    CANCELED = 'CANCELED'
    VALIDATED = 'VALIDATED'

class TicketBase(BaseModel):
    reference: str
    price: float 
    status: Optional[TicketStatus] = TicketStatus.AVAILABLE

    class Config:
        orm_mode = True

class TicketRequest(TicketBase):
    event_id: int
    order_id: Optional[int] = None
    user_id: Optional[int] = None

class TicketResponse(TicketBase):
    id: int
    user: Optional[UserResponse]
    created_at: datetime

    class Config:
        orm_mode = True

class TicketSummary(BaseModel):
    count: Optional[int]
    event: EventResponse
    tickets: List[TicketResponse]
    

    class Config:
        orm_mode = True

class CreateTicket(BaseModel):
    event_id: int
    price: float
    limit: int
