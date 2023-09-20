# from typing import List

# from app.oauth2 import get_current_user
# from ..models import TicketStatusHistoryResponse
# from .. import schemas
# from sqlalchemy.orm import Session
# from ..database import get_db
# from fastapi import Depends, APIRouter

# router = APIRouter(
#     prefix="/ticket_status_history",
#     tags=['TicketStatusHistory']
# )

# @router.get("/{ticket_id}", response_model=List[TicketStatusHistoryResponse])
# async def get_ticket_status_history_by_ticket_id(ticket_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
#     ticket_status_history = (
#         db.query(schemas.TicketStatusHistory)
#         .filter(schemas.TicketStatusHistory.ticket_id == ticket_id)
#         .order_by(schemas.TicketStatusHistory.status_at)
#         .all()
#     )

#     return ticket_status_history