from sqlalchemy.orm import Session
from typing import List
from app.api.models.event import EventRequest
from app.schemas.event import Event
from app.schemas.favourite import Favourite
from datetime import date

class EventRepository:

    @staticmethod
    async def get_all_events(db: Session) -> List[Event]:
        today = date.today()
        events = (
            db.query(Event)
            .filter(Event.date > today)
            .order_by(Event.date, Event.time)
            .all()
        )
        return events

    @staticmethod
    async def get_event_by_id(db: Session, id: int) -> Event:
        return db.query(Event).filter(Event.id == id).first()
    
    @staticmethod
    async def get_event_by_event_request(db: Session, event: EventRequest) -> Event:
        event_db = db.query(Event).filter(Event.title == event.title).filter(Event.date == event.date).filter(Event.time == event.time).first()
        if event_db:
            return event_db

    @staticmethod
    async def get_favourite_events_by_user_id(db: Session, user_id: int) -> List[Event]:
        favorite_events = (
            db.query(Event)
            .join(Favourite)
            .filter(Favourite.user_id == user_id)
            .all()
        )
        return favorite_events

    @staticmethod
    async def get_events_by_organization_id(db: Session, organization_id: int) -> List[Event]:
        return db.query(Event).filter(Event.organization_id == organization_id).all()

    @staticmethod
    async def create_event(db: Session, event: EventRequest) -> Event:
        new_event = Event(**event.dict())
        db.add(new_event)
        db.commit()
        db.refresh(new_event)
        return new_event

    @staticmethod
    async def update_event_by_id(db: Session, id: int, updated_event: EventRequest) -> Event:
        event = db.query(Event).filter(Event.id == id)
        if event.first():
            event.update(updated_event.dict(), synchronize_session=False)
            db.commit()
            return event.first()
        return None

    @staticmethod
    async def delete_event_by_id(db: Session, id: int):
        event = db.query(Event).filter(Event.id == id).first()
        if event:
            db.delete(event)
            db.commit()

    @staticmethod
    async def delete_events_by_organization_id(db: Session, organization_id: int):
        events = db.query(Event).filter(Event.organization_id == organization_id).all()
        for event in events:
            db.delete(event)
        db.commit()

    @staticmethod
    async def delete_all_events(db: Session):
        db.query(Event).delete()
        db.commit()
