from sqlalchemy.orm import Session
from typing import List
from app.models.ticket_status_history import TicketStatusHistoryResponse
from app.core.repositories.ticket_status_history_repository import TicketStatusHistoryRepository

class TicketStatusHistoryService:
    @staticmethod
    def get_ticket_status_history_by_ticket_id(db: Session, ticket_id: int) -> List[TicketStatusHistoryResponse]:
        return TicketStatusHistoryRepository.get_ticket_status_history_by_ticket_id(db, ticket_id)
