from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.services.favourite_service import FavouriteService
from app.database import get_db
from app.oauth2 import get_current_user

router = APIRouter(prefix="/favourites", tags=['favourites'])

@router.post("/{event_id}", status_code=status.HTTP_201_CREATED)
def add_to_favourites(event_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    if FavouriteService.is_event_in_favorites(db, event_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"user {current_user.id} has already added event {event_id} to favorites",
        )

    FavouriteService.add_event_to_favorites(db, event_id, current_user.id)
    return {"message": "Succesfully added to favourites"}

@router.delete("/{event_id}", status_code=status.HTTP_201_CREATED)
def delete_from_favourites(event_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    if not FavouriteService.is_event_in_favorites(db, event_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"event {event_id} does not exist in favorites list",
        )

    FavouriteService.remove_event_from_favorites(db, event_id, current_user.id)
    return {"message": "Succesfully deleted from favourites"}
