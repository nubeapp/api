from sqlalchemy.orm import Session
from app.core.repositories.code_repository import CodeRepository
from app.models.code import CodeRequest
from pydantic import EmailStr

class CodeService:
    @staticmethod
    async def get_codes(db: Session):
        return await CodeRepository.get_codes(db)

    @staticmethod
    async def get_code_by_email(db: Session, email: EmailStr):
        return await CodeRepository.get_code_by_email(db, email)

    @staticmethod
    async def create_code(db: Session, code: CodeRequest):
        return await CodeRepository.create_code(db, code)

    @staticmethod
    async def update_code_by_email(db: Session, email: EmailStr, updated_code: CodeRequest):
        return await CodeRepository.update_code_by_email(db, email, updated_code)

    @staticmethod
    async def delete_code(db: Session, email: str):
        await CodeRepository.delete_code(db, email)

    @staticmethod
    async def delete_all_codes(db: Session):
        await CodeRepository.delete_all_codes(db)
