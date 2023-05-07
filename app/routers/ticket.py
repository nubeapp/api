from typing import List

from app.oauth2 import get_current_user
from ..models import TicketRequest, TicketResponse
from .. import schemas
from sqlalchemy.orm import Session, joinedload
from ..database import get_db
from fastapi import status, HTTPException, Depends, APIRouter

router = APIRouter(
    prefix="/tickets",
    tags=['Tickets']
)

@router.get("/{event_id}", response_model=List[TicketResponse])
async def get_tickets_by_event_id(event_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    tickets = db.query(schemas.Ticket).filter(schemas.Ticket.event_id == event_id).all()
    return tickets

@router.post("", status_code=status.HTTP_201_CREATED, response_model=List[TicketResponse])
async def create_tickets(tickets: List[TicketRequest], db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    new_tickets: List[TicketResponse] = [];
    for i in range(0, len(tickets)):
        new_ticket = schemas.Ticket(**tickets[i].dict())
        new_tickets.append(new_ticket)
        db.add(new_ticket)
        db.commit()
        db.refresh(new_ticket)
    return new_tickets

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ticket_by_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    ticket = db.query(schemas.Ticket).filter(schemas.Ticket.id == id).first()
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No ticket found for id {id}")
    db.delete(ticket)
    db.commit()

