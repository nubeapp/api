from app.models import TicketSummary, ValidationData, TicketStatus
from app.oauth2 import get_current_user
from .. import schemas
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi import status, HTTPException, Depends, APIRouter
from datetime import datetime


router = APIRouter(prefix="/validation", tags=['validation'])

@router.put("", status_code=status.HTTP_200_OK)
async def validate_ticket(validation_data: ValidationData, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    ticket = (
        db.query(schemas.Ticket)
        .filter(schemas.Ticket.event_id == validation_data.event_id)
        .filter(schemas.Ticket.reference == validation_data.reference)
        .first()
    )

    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Ticket with the provided reference was not found.")

    ticket_sold = db.query(schemas.Ticket).filter(schemas.Ticket.event_id == validation_data.event_id).filter(schemas.Ticket.reference == validation_data.reference).filter(schemas.Ticket.status == TicketStatus.SOLD).first()

    if not ticket_sold:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Ticket has been already validated.")
    
    # Update the ticket status to "VALIDATED" if all checks pass
    ticket_sold.status = TicketStatus.VALIDATED
    ticket_sold.validated_at = datetime.now()
    db.commit()

    # Return success response
    return {"message": "ticket validated succesfully"}
