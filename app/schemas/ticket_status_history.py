from app.database import Base
from app.models.ticket import TicketStatus
from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.sql.sqltypes import TIMESTAMP

class TicketStatusHistory(Base):
    __tablename__ = "ticket_status_history"

    id = Column(Integer, primary_key=True, nullable=False)
    ticket_id = Column(Integer, ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(TicketStatus), nullable=False)
    status_at = Column(TIMESTAMP(timezone=True), nullable=False)