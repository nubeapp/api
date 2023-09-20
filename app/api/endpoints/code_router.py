from pydantic import EmailStr
from app.core.services.code_service import CodeService
from app.database import get_db
from app.models.code import CodeRequest, CodeResponse
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter

router = APIRouter(
    prefix="/codes",
    tags=['Codes']
)

@router.get("")
async def get_codes(db: Session = Depends(get_db)):
    codes = await CodeService.get_codes(db)
    return codes

@router.get("/{email}", response_model=CodeResponse)
async def get_code_by_email(email: EmailStr, db: Session = Depends(get_db)):
    code = await CodeService.get_code_by_email(db, email)
    if not code:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The email {email} has no associated code")
    return code

@router.post("", status_code=status.HTTP_201_CREATED, response_model=CodeResponse)
async def create_code(code: CodeRequest, db: Session = Depends(get_db)):
    code_by_email = await CodeService.get_code_by_email(db, code.email)
    if code_by_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"The user has already a code associated")
    new_code = await CodeService.create_code(db, code)
    return new_code

@router.put("/{email}", response_model=CodeResponse)
async def update_code_by_email(email: EmailStr, updated_code: CodeRequest, db: Session = Depends(get_db)):
    code = await CodeService.update_code_by_email(db, email, updated_code)
    return code

@router.delete("/{email}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_code(email: str, db: Session = Depends(get_db)):
    await CodeService.delete_code(db, email)

@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_codes(db: Session = Depends(get_db)):
    await CodeService.delete_all_codes(db)
