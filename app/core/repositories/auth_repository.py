from sqlalchemy.orm import Session
from app.schemas.user import User
from pydantic import EmailStr

class AuthRepository:
    @staticmethod
    async def get_user_by_email(db: Session, email: EmailStr):
        return db.query(User).filter(User.email == email).first()
