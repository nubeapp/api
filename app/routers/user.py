from typing import List

from pydantic import EmailStr
from ..models import UserResponse, UserRequest
from .. import schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi import status, HTTPException, Depends, APIRouter

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.get("", response_model=List[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(schemas.User).all()
    return users

@router.get("/{email}", response_model=UserResponse)
async def get_user_by_email(email: EmailStr, db: Session = Depends(get_db)):
    user = db.query(schemas.User).filter(schemas.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with email {email} was not found")
    return user

@router.get("/id/{id}", response_model=UserResponse)
async def get_user_by_email(id: int, db: Session = Depends(get_db)):
    user = db.query(schemas.User).filter(schemas.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} was not found")
    return user

@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(user: UserRequest, db: Session = Depends(get_db)):

    # Hash the password: user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = schemas.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.put("/{email}", response_model=UserResponse)
async def update_user(email: EmailStr,  updated_user: UserRequest, db: Session = Depends(get_db)):
    user = db.query(schemas.User).filter(schemas.User.email == email)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with email {email} was not found")
    user.update(updated_user.dict(), synchronize_session=False)
    db.commit()
    return user.first()

@router.delete("/{email}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(email: str, db: Session = Depends(get_db)):
    user = db.query(schemas.User).filter(schemas.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with email {email} was not found")
    db.delete(user)
    db.commit()

@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_users(db: Session = Depends(get_db)):
    db.query(schemas.User).delete()
    db.commit()

