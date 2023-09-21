from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.ticket import Ticket
from app.database import get_db
from app.dependencies import insert_ticket_status_history
from app.api.models.ticket import TicketStatus
from app.api.models.validation_data import ValidationData
from functools import wraps

from app.oauth2 import get_current_user

def insert_cancel_ticket_status_history():
    def decorator(fn):
        @wraps(fn)
        async def wrapper(ticket_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
            await insert_ticket_status_history(ticket_id, TicketStatus.CANCELED, db)
            return await fn(ticket_id, db, current_user=current_user)
        return wrapper
    return decorator

def insert_validate_ticket_status_history():
    def decorator(fn):
        @wraps(fn)
        async def wrapper(validation_data: ValidationData, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
            ticket_sold = db.query(Ticket).filter(Ticket.event_id == validation_data.event_id).filter(Ticket.reference == validation_data.reference).filter(Ticket.status == TicketStatus.SOLD).first()

            if not ticket_sold:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail=f"Ticket has been already validated.")
            
            # Update the ticket status to "VALIDATED" if all checks pass
            ticket_sold.status = TicketStatus.VALIDATED
            db.commit()

            await insert_ticket_status_history(ticket_id=ticket_sold.id, ticket_status=TicketStatus.VALIDATED, db=db)

            # Call the original function
            return await fn(validation_data, db, current_user=current_user)
        
        return wrapper
    
    return decorator

cancel_ticket_history = insert_cancel_ticket_status_history()
validate_ticket_history = insert_validate_ticket_status_history()
