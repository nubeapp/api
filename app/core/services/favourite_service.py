from sqlalchemy.orm import Session
from app.core.repositories.favourite_repository import FavouriteRepository

class FavouriteService:

    @staticmethod
    def is_event_in_favorites(db: Session, event_id: int, user_id: int) -> bool:
        return FavouriteRepository.is_event_in_favorites(db, event_id, user_id)

    @staticmethod
    def add_event_to_favorites(db: Session, event_id: int, user_id: int):
        FavouriteRepository.add_event_to_favorites(db, event_id, user_id)

    @staticmethod
    def remove_event_from_favorites(db: Session, event_id: int, user_id: int):
        FavouriteRepository.remove_event_from_favorites(db, event_id, user_id)
