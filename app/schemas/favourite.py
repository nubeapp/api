from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Favourite(Base):
    __tablename__ = "favourites"
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)
    event_id = Column(Integer, ForeignKey(
        "events.id", ondelete="CASCADE"), primary_key=True)
    
    event = relationship("Event")
