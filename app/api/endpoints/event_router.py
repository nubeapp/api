from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.oauth2 import get_current_user
from app.database import get_db
from sqlalchemy.orm import Session
from app.core.services.event_service import EventService
from app.models.event import EventRequest, EventResponse

router = APIRouter(
    prefix="/events",
    tags=['Events']
)

@router.get("", response_model=List[EventResponse])
async def get_all_events(db: Session = Depends(get_db)):
    events = await EventService.get_all_events(db)
    return events

@router.get("/event/{id}", response_model=EventResponse)
async def get_event_by_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    event = await EventService.get_event_by_id(db, id)
    if not event:
        raise HTTPException(status_code=404, detail=f"No event found for id {id}")
    return event

@router.get("/favourites", response_model=List[EventResponse])
async def get_favourite_events_by_user_id(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    favourite_events = await EventService.get_favourite_events_by_user_id(db, current_user.id)
    return favourite_events

@router.get("/{organization_id}", response_model=List[EventResponse])
async def get_events_by_organization_id(organization_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    events = await EventService.get_events_by_organization_id(db, organization_id)
    if not events:
        raise HTTPException(status_code=404, detail=f"No events found for organization_id {organization_id}")
    return events

@router.post("", status_code=201, response_model=EventResponse)
async def create_event(event: EventRequest, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    event_db = await EventService.get_event_by_event_request(db, event)
    if event_db:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Event already exists in database")
    new_event = await EventService.create_event(db, event)
    return new_event

@router.put("/{id}", response_model=EventResponse)
async def update_event_by_id(id: int, updated_event: EventRequest, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    event = await EventService.update_event_by_id(db, id, updated_event)
    if not event:
        raise HTTPException(status_code=404, detail=f"No event found for id {id}")
    return event

@router.delete("/event/{id}", status_code=204)
async def delete_event_by_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    await EventService.delete_event_by_id(db, id)

@router.delete("/{organization_id}", status_code=204)
async def delete_events_by_organization_id(organization_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    await EventService.delete_events_by_organization_id(db, organization_id)

@router.delete("", status_code=204)
async def delete_all_events(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    await EventService.delete_all_events(db)
