# core/repositories/code_repository.py

from sqlalchemy.orm import Session
from app.schemas.code import Code
from app.models.code import CodeRequest
from pydantic import EmailStr

class CodeRepository:
    @staticmethod
    async def get_codes(db: Session):
        return db.query(Code).all()

    @staticmethod
    async def get_code_by_email(db: Session, email: EmailStr):
        return db.query(Code).filter(Code.email == email).first()

    @staticmethod
    async def create_code(db: Session, code: CodeRequest):
        new_code = Code(**code.dict())
        db.add(new_code)
        db.commit()
        db.refresh(new_code)
        return new_code

    @staticmethod
    async def update_code_by_email(db: Session, email: EmailStr, updated_code: CodeRequest):
        code = db.query(Code).filter(Code.email == email)
        if not code.first():
            return None
        code.update(updated_code.dict(), synchronize_session=False)
        db.commit()
        return code.first()

    @staticmethod
    async def delete_code(db: Session, email: str):
        code = db.query(Code).filter(Code.email == email).first()
        if code:
            db.delete(code)
            db.commit()

    @staticmethod
    async def delete_all_codes(db: Session):
        db.query(Code).delete()
        db.commit()
