from datetime import datetime
from pydantic import BaseModel

from app.models.ticket import TicketStatus

class TicketStatusHistoryResponse(BaseModel):
    id: int
    ticket_id: int
    status: TicketStatus
    status_at: datetime

    class Config:
        orm_mode = True
