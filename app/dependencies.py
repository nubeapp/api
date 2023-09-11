from fastapi import Depends
from sqlalchemy.orm import Session
from app import schemas
from datetime import datetime

from app.database import get_db

async def insert_ticket_status_history(ticket_id: int, ticket_status: str, db: Session = Depends(get_db)):
    new_ticket_status_history = schemas.TicketStatusHistory(ticket_id=ticket_id, status=ticket_status, status_at=datetime.now())
    db.add(new_ticket_status_history)
    db.commit()
    db.refresh(new_ticket_status_history)
