from sqlalchemy.orm import Session
from typing import List, Optional
from app.api.models.ticket import TicketSummary, CreateTicket
from app.api.models.order import OrderRequest
from app.core.repositories.ticket_repository import TicketRepository

class TicketService:
    @staticmethod
    async def get_tickets_by_user_id(
        db: Session,
        user_id: int,
        limit: int,
        offset: int
    ) -> List[TicketSummary]:
        return await TicketRepository.get_tickets_by_user_id(db, user_id, limit, offset)

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
        return await TicketRepository.get_tickets_by_event_id(db, event_id, user_id, limit, offset, status, filter)

    @staticmethod
    async def get_tickets_available_by_event_id(
        db: Session,
        event_id: int
    ) -> TicketSummary:
        return await TicketRepository.get_tickets_available_by_event_id(db, event_id)

    @staticmethod
    async def get_tickets_by_user_id_event_id(
        db: Session,
        event_id: int,
        user_id: int
    ) -> TicketSummary:
        return await TicketRepository.get_tickets_by_user_id_event_id(db, event_id, user_id)

    @staticmethod
    async def create_tickets(
        db: Session,
        ticket_data: CreateTicket
    ) -> TicketSummary:
        return await TicketRepository.create_tickets(db, ticket_data)

    @staticmethod
    async def buy_ticket(
        db: Session,
        order: OrderRequest,
        user_id: int
    ) -> TicketSummary:
        return await TicketRepository.buy_ticket(db, order, user_id)

    @staticmethod
    async def cancel_ticket(
        db: Session,
        ticket_id: int
    ) -> None:
        return await TicketRepository.cancel_ticket(db, ticket_id)

    @staticmethod
    async def delete_ticket_by_id(
        db: Session,
        id: int
    ) -> None:
        return await TicketRepository.delete_ticket_by_id(db, id)

    @staticmethod
    async def delete_tickets_by_event_id(
        db: Session,
        event_id: int
    ) -> None:
        return await TicketRepository.delete_tickets_by_event_id(db, event_id)
