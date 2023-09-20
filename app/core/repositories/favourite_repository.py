from sqlalchemy.orm import Session
from app.schemas.favourite import Favourite

class FavouriteRepository:

    @staticmethod
    def is_event_in_favorites(db: Session, event_id: int, user_id: int) -> bool:
        return (
            db.query(Favourite)
            .filter(Favourite.event_id == event_id, Favourite.user_id == user_id)
            .first() is not None
        )

    @staticmethod
    def add_event_to_favorites(db: Session, event_id: int, user_id: int):
        favorite = Favourite(event_id=event_id, user_id=user_id)
        db.add(favorite)
        db.commit()

    @staticmethod
    def remove_event_from_favorites(db: Session, event_id: int, user_id: int):
        db.query(Favourite).filter(
            Favourite.event_id == event_id, Favourite.user_id == user_id
        ).delete()
        db.commit()
