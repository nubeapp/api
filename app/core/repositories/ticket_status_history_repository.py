from sqlalchemy.orm import Session
from typing import List
from app.api.models.ticket_status_history import TicketStatusHistoryResponse
from app.schemas.ticket_status_history import TicketStatusHistory

class TicketStatusHistoryRepository:
    @staticmethod
    def get_ticket_status_history_by_ticket_id(db: Session, ticket_id: int) -> List[TicketStatusHistoryResponse]:
        ticket_status_history = (
            db.query(TicketStatusHistory)
            .filter(TicketStatusHistory.ticket_id == ticket_id)
            .order_by(TicketStatusHistory.status_at)
            .all()
        )
        return ticket_status_history
