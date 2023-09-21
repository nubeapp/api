from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.oauth2 import get_current_user
from app.api.models.ticket_status_history import TicketStatusHistoryResponse
from app.core.services.ticket_status_history_service import TicketStatusHistoryService

router = APIRouter(
    prefix="/ticket_status_history",
    tags=['TicketStatusHistory']
)

@router.get("/{ticket_id}", response_model=List[TicketStatusHistoryResponse])
async def get_ticket_status_history_by_ticket_id(ticket_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    ticket_status_history = TicketStatusHistoryService.get_ticket_status_history_by_ticket_id(db, ticket_id)
    return ticket_status_history
