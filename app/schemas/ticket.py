from app.database import Base
from app.models.ticket import TicketStatus
from sqlalchemy import Column, String, Integer, ForeignKey, Double, Enum
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, nullable=False)
    reference = Column(String, nullable=False)
    price = Column(Double, nullable=False)
    status = Column(Enum(TicketStatus), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))

    event = relationship("Event")
    user = relationship("User")
    order = relationship("Order")
