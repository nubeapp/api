# from app.models import EventResponse
# from app.oauth2 import get_current_user
# from app.routers.event import get_event_by_id
# from .. import schemas
# from sqlalchemy.orm import Session
# from ..database import get_db
# from fastapi import status, HTTPException, Depends, APIRouter
# from typing import List


# router = APIRouter(prefix="/favourites", tags=['favourites'])

# @router.post("/{event_id}", status_code=status.HTTP_201_CREATED)
# def add_to_favourites(event_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
#     # Search the event. If it does not exist, user cannot vote it
#     event = db.query(schemas.Event).filter(schemas.Event.id == event_id).first()
#     if not event:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"event with id {event_id} does not exist")
    
#     # Search if user has already added to favourite this event
#     favourite_query = db.query(schemas.Favourite).filter(
#         schemas.Favourite.event_id == event_id, schemas.Favourite.user_id == current_user.id)
#     found_favourite = favourite_query.first()

#     # If he had already add to favourites the event, he cannot added it again, so raise HTTPException
#     if found_favourite:  
#             raise HTTPException(status_code=status.HTTP_409_CONFLICT,
#                                 detail=f"user {current_user.id} has already add to favourites the event {event_id}")
    
#     # If not, add the event to favourites table
#     new_favourite = schemas.Favourite(event_id=event_id, user_id=current_user.id)
#     db.add(new_favourite)
#     db.commit()
#     return {"message": "Succesfully added to favourites"}

# @router.delete("/{event_id}", status_code=status.HTTP_201_CREATED)
# def delete_from_favourites(event_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
#     # Search the event. If it does not exist, user cannot vote it
#     event = db.query(schemas.Event).filter(schemas.Event.id == event_id).first()
#     if not event:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"event with id {event_id} does not exist")
    
#     # Search if user has already added to favourite this event
#     favourite_query = db.query(schemas.Favourite).filter(
#         schemas.Favourite.event_id == event_id, schemas.Favourite.user_id == current_user.id)
#     found_favourite = favourite_query.first()

#     # If he had already add to favourites the event, he cannot added it again, so raise HTTPException
#     if not found_favourite:  
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                 detail=f"event {event_id} does not exists in favourites list")
    
#     # If not, add the event to favourites table
#     favourite_query.delete(synchronize_session=False)
#     db.commit()
#     return {"message": "Succesfully deleted from favourites"}
