from typing import List

from pydantic import EmailStr
from ..models import AssistantBase, UserCreate
from .. import schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi import status, HTTPException, Depends, APIRouter
from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/assistants",
    tags=['Assistants']
)

@router.get("")
async def get_assistants(db: Session = Depends(get_db)):
    assistants = db.query(schemas.Assistant).all()
    return assistants

@router.post("", status_code=status.HTTP_201_CREATED)
async def assist(assistant: AssistantBase, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    
    # Search the event. If it does not exists, you cannot attend
    event = db.query(schemas.Event).filter(schemas.Event.id == assistant.event_id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'event with id {assistant.event_id} does not exists')
    
    # Search if the user_id is already assisting
    assistant_query = db.query(schemas.Assistant).filter(schemas.Assistant.event_id == assistant.event_id, schemas.Assistant.user_id == current_user.id)
    found_assistant = assistant_query.first()
    if (assistant.dir == 1):
        if found_assistant:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'user {current_user.id} is already assisting the event {assistant.event_id}')
        
        new_assistant = schemas.Assistant(user_id=current_user.id, event_id=assistant.event_id)
        db.add(new_assistant)
        db.commit()
        return {"message": f"user {new_assistant.user_id} assisting event {new_assistant.event_id}"}
    else:
        if not found_assistant:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user {current_user.id} was not assisting the event {assistant.event_id}')
        assistant_query.delete(synchronize_session=False)
        db.commit()
        return {"message": f"user {current_user.id} not assisting anymore to event"}