from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.decorators import cancel_ticket_history

from app.database import get_db
from app.oauth2 import get_current_user
from app.api.models.ticket import (
    TicketSummary,
    CreateTicket,
)
from app.api.models.order import OrderRequest
from app.core.services.ticket_service import TicketService

router = APIRouter(
    prefix="/tickets",
    tags=['Tickets']
)

@router.get("", response_model=List[TicketSummary])
async def get_tickets_by_user_id(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0)
):
    return await TicketService.get_tickets_by_user_id(db, current_user.id, limit, offset)

@router.get("/{event_id}", response_model=TicketSummary)
async def get_tickets_by_event_id(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
    limit: int = None,
    offset: int = None,
    status: Optional[str] = None,
    filter: Optional[str] = None
):
    return await TicketService.get_tickets_by_event_id(db, event_id, current_user.id, limit, offset, status, filter)

@router.get("/available/{event_id}", response_model=TicketSummary)
async def get_tickets_available_by_event_id(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    return await TicketService.get_tickets_available_by_event_id(db, event_id)

@router.get("/events/{event_id}", response_model=TicketSummary)
async def get_tickets_by_user_id_event_id(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    return await TicketService.get_tickets_by_user_id_event_id(db, event_id, current_user.id)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=TicketSummary)
async def create_tickets(
    ticket_data: CreateTicket,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    return await TicketService.create_tickets(db, ticket_data)

@router.post("/buy", status_code=status.HTTP_201_CREATED, response_model=TicketSummary)
async def buy_ticket(
    order: OrderRequest,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    return await TicketService.buy_ticket(db, order, current_user.id)

@router.put("/cancel/{ticket_id}", status_code=status.HTTP_200_OK)
@cancel_ticket_history
async def cancel(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    await TicketService.cancel_ticket(db, ticket_id)
    return {"message": "ticket has been cancelled successfully"}

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ticket_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    return await TicketService.delete_ticket_by_id(db, id)

@router.delete("/event/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tickets_by_event_id(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    return await TicketService.delete_tickets_by_event_id(db, event_id)
