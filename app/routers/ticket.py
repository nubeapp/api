from typing import List

from sqlalchemy import Transaction

from app.oauth2 import get_current_user
from app.routers import event
from app.routers.order import create_order
from ..models import OrderRequest, TicketRequest, TicketResponse, TicketStatus, CreateTicket, TicketSummary
from .. import schemas
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.exc import SQLAlchemyError

from app import helpers, models
from app.logger import get_custom_logger

router = APIRouter(
    prefix="/tickets",
    tags=['Tickets']
)

TICKET_LIMIT: str = 4
logger = get_custom_logger(__name__)

@router.get("", response_model=List[TicketSummary])
async def get_tickets_by_user_id(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    ticket_summaries = []
    
    events = (
        db.query(schemas.Event)
        .join(schemas.Ticket)
        .filter(schemas.Ticket.user_id == current_user.id)
        .distinct()
        .all()
    )
    
    for event in events:
        tickets = (
            db.query(schemas.Ticket)
            .filter(schemas.Ticket.event_id == event.id)
            .filter(schemas.Ticket.user_id == current_user.id)
            .all()
        )
        
        ticket_summaries.append(TicketSummary(event=event, tickets=tickets))
    
    return ticket_summaries

@router.get("/{event_id}", response_model=TicketSummary)
async def get_tickets_by_event_id(event_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    tickets = (
        db.query(schemas.Ticket)
        .filter(schemas.Ticket.event_id == event_id)
        .all()
    )
    event_by_id = await event.get_event_by_id(id=event_id, db=db)
    return TicketSummary(event=event_by_id, tickets=tickets)

@router.get("/available/{event_id}", response_model=TicketSummary)
async def get_tickets_available_by_event_id(event_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    tickets = (
        db.query(schemas.Ticket)
        .filter(schemas.Ticket.event_id == event_id)
        .filter(schemas.Ticket.status == TicketStatus.AVAILABLE)
        .all()
    )
    event_by_id = await event.get_event_by_id(id=event_id, db=db)
    return TicketSummary(event=event_by_id, tickets=tickets)

@router.get("/events/{event_id}", response_model=TicketSummary)
async def get_tickets_by_user_id_event_id(event_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    tickets = (
        db.query(schemas.Ticket)
        .filter(schemas.Ticket.user_id == current_user.id)
        .filter(schemas.Ticket.event_id == event_id)
        .all()
    )
    event_by_id = await event.get_event_by_id(id=event_id, db=db)
    return TicketSummary(event=event_by_id, tickets=tickets)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=List[TicketSummary])
async def create_tickets(ticket_data: CreateTicket, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    tickets_gen = generate_tickets_by_event(
        event_id=ticket_data.event_id,
        price=ticket_data.price,
        limit=ticket_data.limit
    )
    new_tickets: List[TicketResponse] = []
    
    for i in range(len(tickets_gen)):
        new_ticket = schemas.Ticket(**tickets_gen[i].dict())
        new_tickets.append(new_ticket)
        db.add(new_ticket)
        db.commit()
        db.refresh(new_ticket)
    
    event_by_id = await event.get_event_by_id(id=ticket_data.event_id, db=db)
    return [TicketSummary(event=event_by_id, tickets=new_tickets)]

@router.post("/buy", status_code=status.HTTP_201_CREATED, response_model=List[TicketSummary])
async def buy_ticket(order: OrderRequest, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    try:
        # Check if the event exists
        event_db = await event.get_event_by_id(id=order.event_id, db=db)
        if not event_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Event {order.event_id} does not exist')
        
        # Check if the quantity is greater than 0
        if order.quantity <= 0:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='The quantity of tickets should be more than 0 and less than TICKET_LIMIT')
        
        # Check if the current user has reached the limit of tickets for one person
        user_tickets = await get_tickets_by_user_id_event_id(event_id=event_db.id, db=db, current_user=current_user)
        logger.info(f"user_tickets: {len(user_tickets.tickets)}")
        logger.info(f"quantity: {order.quantity}")
        if len(user_tickets.tickets) + order.quantity > TICKET_LIMIT:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Users can purchase a limit of 4 tickets')
        
        # Check if there are enough tickets available
        tickets_available = await get_tickets_available_by_event_id(event_id=order.event_id, db=db)
        if len(tickets_available.tickets) < order.quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'There are not enough tickets for event {order.event_id}')
        
        # Create the order
        if order.quantity > 0:
            new_order = await create_order(user_id=current_user.id, db=db)
        
        # Get the tickets
        tickets = (
            db.query(schemas.Ticket)
            .filter(schemas.Ticket.event_id == event_db.id)
            .filter(schemas.Ticket.status == TicketStatus.AVAILABLE)
            .limit(order.quantity)
            .all()
        )
        
        # Update the ticket sold property
        for ticket in tickets:
            updated_ticket = models.TicketRequest(
                reference=ticket.reference,
                price=ticket.price,
                status=TicketStatus.SOLD,
                user_id=current_user.id,
                order_id=new_order.id,
                event_id=ticket.event_id
            )
            await update_ticket_by_id(ticket_id=ticket.id, updated_ticket=updated_ticket, db=db)
        
        return [TicketSummary(event=event_db, tickets=tickets)]
    
    except SQLAlchemyError as error:
        logger.error(error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database Error")

async def update_ticket_by_id(ticket_id: int, updated_ticket: TicketRequest, db: Session = Depends(get_db)):
    ticket = db.query(schemas.Ticket).filter(schemas.Ticket.id == ticket_id)
    if not ticket.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"ticket with id {ticket_id} was not found")
    ticket.update(updated_ticket.dict(), synchronize_session=False)
    db.commit()

def generate_tickets_by_event(event_id: int, price: float, limit: int):
    references = helpers.generate_random_reference_list_by_limit(limit)
    tickets: List[TicketRequest] = []
    for reference in references:
        ticket = TicketRequest(
            price=price,
            reference=reference,
            event_id=event_id,
            status=TicketStatus.AVAILABLE
        )
        tickets.append(ticket)
    return tickets
