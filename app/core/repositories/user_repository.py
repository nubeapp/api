from sqlalchemy.orm import Session
from app.schemas.user import User
from app.models.user import UserRequest, EmailStr

class UserRepository:
    @staticmethod
    async def get_all_users(db: Session):
        return db.query(User).all()

    @staticmethod
    async def get_user_by_email(db: Session, email: EmailStr):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    async def get_user_by_id(db: Session, id: int):
        return db.query(User).filter(User.id == id).first()

    @staticmethod
    async def create_user(db: Session, user: UserRequest):
        db_user = User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    async def update_user(db_user: User, updated_user: UserRequest, db: Session):
        for key, value in updated_user.dict().items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    async def delete_user(db: Session, user: User):
        db.delete(user)
        db.commit()

    @staticmethod
    async def delete_all_users(db: Session):
        db.query(User).delete()
        db.commit()
