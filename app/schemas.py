from app.models import TicketStatus
from .database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Double, Enum
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    
class Code(Base):
    __tablename__ = "codes"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    code = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    
class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    date = Column(TIMESTAMP(timezone=True), nullable=False)
    time = Column(String, nullable=False)
    venue = Column(String, nullable=False)
    ticket_limit = Column(Integer, nullable=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))

    organization = relationship("Organization")

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))

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

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, nullable=False)
    order_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))

    user = relationship("User")

