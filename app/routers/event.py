from collections import defaultdict
from datetime import date
from typing import List

from app.oauth2 import get_current_user
from ..models import EventRequest, EventResponse
from .. import schemas
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi import status, HTTPException, Depends, APIRouter

router = APIRouter(
    prefix="/events",
    tags=['Events']
)

@router.get("", response_model=List[EventResponse])
async def get_all_events(db: Session = Depends(get_db)):
    today = date.today()
    events = (
        db.query(schemas.Event)
        .filter(schemas.Event.date > today)
        .order_by(schemas.Event.date, schemas.Event.time)
        .all()
    )
    return events

# @router.get("", response_model=List[EventResponse])
# async def get_all_events(db: Session = Depends(get_db)):
#     events = db.query(schemas.Event).order_by(schemas.Event.date, schemas.Event.time).all()
#     return events

@router.get("/event/{id}", response_model=EventResponse)
async def get_event_by_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    event = db.query(schemas.Event).filter(schemas.Event.id == id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No event found for id {id}")
    return event

@router.get("/favourites", response_model=List[EventResponse])
async def get_favourite_events_by_user_id(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    favourite_events = db.query(schemas.Event).join(schemas.Favourite, schemas.Favourite.event_id == schemas.Event.id).filter(schemas.Favourite.user_id == current_user.id).all()
    return favourite_events

@router.get("/{organization_id}", response_model=List[EventResponse])
async def get_events_by_organization_id(organization_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    events = db.query(schemas.Event).filter(schemas.Event.organization_id == organization_id).all()
    if len(events) <= 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No event found for organization_id {organization_id}")
    return events

@router.post("", status_code=status.HTTP_201_CREATED, response_model=EventResponse)
async def create_event(event: EventRequest, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    new_event = schemas.Event(**event.dict())
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

@router.put("/{id}", response_model=EventResponse)
async def update_event_by_id(id: int, updated_event: EventRequest, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    event = db.query(schemas.Event).filter(schemas.Event.id == id)
    if not event.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No event found for id {id}")
    event.update(updated_event.dict(), synchronize_session=False)
    db.commit()
    return event.first()

@router.delete("/event/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event_by_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    event = db.query(schemas.Event).filter(schemas.Event.id == id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No event found for id {id}")
    db.delete(event)
    db.commit()

@router.delete("/{organization_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_events_by_organization_id(organization_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    events = db.query(schemas.Event).filter(schemas.Event.organization_id == organization_id).all()
    if not events:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No events found for organization_id {organization_id}")
    for event in events:
        db.delete(event)
    db.commit()

@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_events(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    db.query(schemas.Event).delete()
    db.commit()
