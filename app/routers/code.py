from typing import List

from pydantic import EmailStr
from ..models import CodeRequest, CodeResponse
from .. import schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi import status, HTTPException, Depends, APIRouter

router = APIRouter(
    prefix="/codes",
    tags=['Codes']
)

@router.get("")
async def get_codes(db: Session = Depends(get_db)):
    codes = db.query(schemas.Code).all()
    return codes

@router.get("/{email}", response_model=CodeResponse)
async def get_code_by_email(email: EmailStr, db: Session = Depends(get_db)):
    code = db.query(schemas.Code).filter(schemas.Code.email == email).first()
    if not code:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The email {email} has not code associated")
    return code

@router.post("", status_code=status.HTTP_201_CREATED, response_model=CodeResponse)
async def create_code(code: CodeRequest, db: Session = Depends(get_db)):
    new_code = schemas.Code(**code.dict())
    db.add(new_code)
    db.commit()
    db.refresh(new_code)
    return new_code

@router.put("/{email}", response_model=CodeResponse)
async def update_code_by_email(email: EmailStr, updated_code: CodeRequest, db: Session = Depends(get_db)):
    code = db.query(schemas.Code).filter(schemas.Code.email == email)
    if not code.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The email {email} has not code associated")
    code.update(updated_code.dict(), synchronize_session=False)
    db.commit()
    return code.first()

@router.delete("/{email}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_code(email: str, db: Session = Depends(get_db)):
    code = db.query(schemas.Code).filter(schemas.Code.email == email).first()
    if not code:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The email {email} has not code associated")
    db.delete(code)
    db.commit()

@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_codes(db: Session = Depends(get_db)):
    db.query(schemas.Code).delete()
    db.commit()
