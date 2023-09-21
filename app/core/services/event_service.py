from typing import List
from sqlalchemy.orm import Session
from app.api.models.event import EventRequest, EventResponse
from app.core.repositories.event_repository import EventRepository

class EventService:

    @staticmethod
    async def get_all_events(db: Session) -> List[EventResponse]:
        events = await EventRepository.get_all_events(db)
        return events

    @staticmethod
    async def get_event_by_id(db: Session, id: int) -> EventResponse:
        event = await EventRepository.get_event_by_id(db, id)
        if event:
            return event
        
    @staticmethod
    async def get_event_by_event_request(db: Session, event: EventRequest) -> EventResponse:
        event = await EventRepository.get_event_by_event_request(db, event)
        if event:
            return event

    @staticmethod
    async def get_favourite_events_by_user_id(db: Session, user_id: int) -> List[EventResponse]:
        favorite_events = await EventRepository.get_favourite_events_by_user_id(db, user_id)
        return favorite_events

    @staticmethod
    async def get_events_by_organization_id(db: Session, organization_id: int) -> List[EventResponse]:
        events = await EventRepository.get_events_by_organization_id(db, organization_id)
        return events

    @staticmethod
    async def create_event(db: Session, event: EventRequest) -> EventResponse:
        new_event = await EventRepository.create_event(db, event)
        return new_event

    @staticmethod
    async def update_event_by_id(db: Session, id: int, updated_event: EventRequest) -> EventResponse:
        event = await EventRepository.update_event_by_id(db, id, updated_event)
        if event:
            return event

    @staticmethod
    async def delete_event_by_id(db: Session, id: int):
        await EventRepository.delete_event_by_id(db, id)

    @staticmethod
    async def delete_events_by_organization_id(db: Session, organization_id: int):
        await EventRepository.delete_events_by_organization_id(db, organization_id)

    @staticmethod
    async def delete_all_events(db: Session):
        await EventRepository.delete_all_events(db)
