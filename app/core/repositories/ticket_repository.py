from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import Depends, HTTPException, status
from app import helpers, logger
from app.dependencies import insert_ticket_status_history
from app.api.models.ticket import TicketStatus
from app.oauth2 import get_current_user
from app.schemas.ticket import Ticket
from app.schemas.event import Event
from app.api.models.ticket import TicketSummary, CreateTicket, TicketRequest, TicketResponse
from app.api.models.order import OrderRequest
from sqlalchemy.exc import SQLAlchemyError
from app.core.repositories.order_repository import OrderRepository
from app.core.services.event_service import EventService
from app.decorators import cancel_ticket_history

class TicketRepository:

    TICKET_LIMIT: str = 4

    @staticmethod
    async def get_tickets_by_user_id(
        db: Session,
        user_id: int,
        limit: int,
        offset: int
    ) -> List[TicketSummary]:
        ticket_summaries = []
    
        events = (
            db.query(Event)
            .join(Ticket)
            .filter(Ticket.user_id == user_id)
            .distinct(Event.id)
            .offset(offset)
            .limit(limit)
            .all()
        )
        
        for event in events:
            tickets = (
                db.query(Ticket)
                .filter(Ticket.event_id == event.id)
                .filter(Ticket.user_id == user_id)
                .all()
            )
            
            ticket_summaries.append(TicketSummary(event=event, tickets=tickets, count=len(tickets)))
        
        return ticket_summaries

    @staticmethod
    async def get_tickets_by_event_id(
        db: Session,
        event_id: int,
        user_id: int,
        limit: int,
        offset: int,
        status: Optional[str],
        filter: Optional[str]
    ) -> TicketSummary:
        query = db.query(Ticket).filter(Ticket.event_id == event_id)

        if status is not None:
            query = query.filter(Ticket.status == status)
        if filter is not None:
            query = query.filter(Ticket.reference.startswith(filter))

        count = query.count()

        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)

        tickets = query.all()

        event_by_id = db.query(Event).filter(Event.id == event_id).first()
        return TicketSummary(event=event_by_id, tickets=tickets, count=count)

    @staticmethod
    async def get_tickets_available_by_event_id(
        db: Session,
        event_id: int
    ) -> TicketSummary:
        tickets = (
            db.query(Ticket)
            .filter(Ticket.event_id == event_id)
            .filter(Ticket.status == "AVAILABLE")
            .all()
        )
        event_by_id = db.query(Event).filter(Event.id == event_id).first()
        return TicketSummary(event=event_by_id, tickets=tickets, count=len(tickets))

    @staticmethod
    async def get_tickets_by_user_id_event_id(
        db: Session,
        event_id: int,
        user_id: int
    ) -> TicketSummary:
        tickets = (
            db.query(Ticket)
            .filter(Ticket.user_id == user_id)
            .filter(Ticket.event_id == event_id)
            .all()
        )
        event_by_id = db.query(Event).filter(Event.id == event_id).first()
        return TicketSummary(event=event_by_id, tickets=tickets, count=len(tickets))

    @staticmethod
    async def create_tickets(
        db: Session,
        ticket_data: CreateTicket
    ) -> TicketSummary:
        event_db = db.query(Event).filter(Event.id == ticket_data.event_id).first()
        if not event_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Event {ticket_data.event_id} does not exist')
        tickets_gen = await TicketRepository.generate_tickets_by_event(
            event_id=ticket_data.event_id,
            price=ticket_data.price,
            limit=ticket_data.limit
        )
        new_tickets: List[TicketResponse] = []

        for i in range(len(tickets_gen)):
            new_ticket = Ticket(**tickets_gen[i].dict())
            new_tickets.append(new_ticket)
            db.add(new_ticket)
            db.commit()
            db.refresh(new_ticket)
            await insert_ticket_status_history(ticket_id=new_ticket.id, ticket_status=TicketStatus.AVAILABLE, db=db)

        # event_by_id = db.query(Event).filter(Event.id == ticket_data.event_id).first()
        event_by_id = await EventService.get_event_by_id(db, ticket_data.event_id)
        return TicketSummary(count=ticket_data.limit, event=event_by_id, tickets=new_tickets)

    @staticmethod
    async def buy_ticket(
        db: Session,
        order: OrderRequest,
        user_id: int
    ) -> TicketSummary:
        try:
            # Check if the event exists
            event_db = await EventService.get_event_by_id(db, order.event_id)
            if not event_db:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Event {order.event_id} does not exist')

            # Check if the quantity is greater than 0
            if order.quantity <= 0:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='The quantity of tickets should be more than 0 and less than TICKET_LIMIT')

            # Check if the current user has reached the limit of tickets for one person
            user_tickets = await TicketRepository.get_tickets_by_user_id_event_id(event_id=event_db.id, db=db, user_id=user_id)
            if len(user_tickets.tickets) + order.quantity > TicketRepository.TICKET_LIMIT:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Users can purchase a limit of 4 tickets')

            # Check if there are enough tickets available
            tickets_available = await TicketRepository.get_tickets_available_by_event_id(event_id=order.event_id, db=db)
            if len(tickets_available.tickets) < order.quantity:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'There are not enough tickets for event {order.event_id}')

            # Create the order
            if order.quantity > 0:
                new_order = await OrderRepository.create_order(user_id=user_id, db=db)

            # Get the tickets
            tickets = (
                db.query(Ticket)
                .filter(Ticket.event_id == event_db.id)
                .filter(Ticket.status == TicketStatus.AVAILABLE)
                .limit(order.quantity)
                .all()
            )

            # Update the ticket sold property
            for ticket in tickets:
                updated_ticket = TicketRequest(
                    reference=ticket.reference,
                    price=ticket.price,
                    status="SOLD",
                    user_id=user_id,
                    order_id=new_order.id,
                    event_id=ticket.event_id,
                )
                await TicketRepository.update_ticket_by_id(ticket_id=ticket.id, updated_ticket=updated_ticket, db=db)
                await insert_ticket_status_history(ticket_id=ticket.id, ticket_status=TicketStatus.SOLD, db=db)

            return TicketSummary(event=event_db, tickets=tickets, count=len(tickets))

        except SQLAlchemyError as error:
            logger.error(error)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database Error")

    @staticmethod
    async def cancel_ticket(
        db: Session,
        ticket_id: int,
    ) -> None:
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No ticket found for id {id}")
        if ticket.status == "CANCELED":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"The ticket is already canceled")
        if ticket.status == "VALIDATED":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Cannot cancel a validated ticket")
        ticket.status = "CANCELED"
        db.commit()

    @staticmethod
    async def delete_ticket_by_id(
        db: Session,
        id: int
    ) -> None:
        ticket = db.query(Ticket).filter(Ticket.id == id).first()
        if not ticket:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No ticket found for id {id}")
        db.delete(ticket)
        db.commit()

    @staticmethod
    async def delete_tickets_by_event_id(
        db: Session,
        event_id: int
    ) -> None:
        tickets = db.query(Ticket).filter(Ticket.event_id == event_id).all()
        if not tickets:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No tickets found for event_id {event_id}")
        for ticket in tickets:
            db.delete(ticket)
        db.commit()

    @staticmethod
    async def update_ticket_by_id(
        db: Session,
        ticket_id: int,
        updated_ticket: TicketRequest
    ) -> None:
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id)
        if not ticket.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ticket with id {ticket_id} was not found")
        ticket.update(updated_ticket.dict(), synchronize_session=False)
        db.commit()

    @staticmethod
    async def generate_tickets_by_event(
        event_id: int,
        price: float,
        limit: int
    ) -> List[TicketRequest]:
        references = helpers.generate_random_reference_list_by_limit(limit)
        tickets: List[TicketRequest] = []
        for reference in references:
            ticket = TicketRequest(
                price=price,
                reference=reference,
                event_id=event_id,
                status="AVAILABLE"
            )
            tickets.append(ticket)
        return tickets
