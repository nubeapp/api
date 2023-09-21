from sqlalchemy.orm import Session
from app.api.models.ticket import TicketStatus
from app.api.models.validation_data import ValidationData
from app.schemas.ticket import Ticket
from fastapi import HTTPException, status

class ValidationRepository:
    @staticmethod
    async def validate_ticket(db: Session, validation_data: ValidationData, user_id: int):
        ticket = db.query(Ticket).filter(
            Ticket.reference == validation_data.reference,
            Ticket.event_id == validation_data.event_id,
        ).first()

        if not ticket:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found or already used.")
