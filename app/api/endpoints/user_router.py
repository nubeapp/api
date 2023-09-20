from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.services.user_service import UserService
from app.core.repositories.user_repository import UserRepository
from app.database import get_db
from app.models.user import UserResponse, UserRequest, EmailStr
from app.schemas.user import User
from app.utils import check_404

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.get("", response_model=List[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    users = await UserRepository.get_all_users(db)
    return users

@router.get("/{email}", response_model=UserResponse)
async def get_user_by_email(email: EmailStr, db: Session = Depends(get_db)):
    user = await UserRepository.get_user_by_email(db, email)
    check_404(user, email)
    return user

@router.get("/id/{id}", response_model=UserResponse)
async def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = await UserRepository.get_user_by_id(db, id)
    check_404(user, str(id))
    return user

@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(user: UserRequest, db: Session = Depends(get_db)):
    user.password = await UserService.hashed_password(user.password)
    new_user = await UserRepository.create_user(db, user)
    return new_user

@router.put("/{email}", response_model=UserResponse)
async def update_user(email: EmailStr, updated_user: UserRequest, db: Session = Depends(get_db)):
    user = await UserRepository.get_user_by_email(db, email)
    check_404(user, email)
    updated_user.password = await UserService.hashed_password(updated_user.password)
    user = await UserRepository.update_user(user, updated_user, db)
    return user

@router.delete("/{email}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(email: EmailStr, db: Session = Depends(get_db)):
    user = await UserRepository.get_user_by_email(db, email)
    check_404(user, email)

    await UserRepository.delete_user(db, user)

@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_users(db: Session = Depends(get_db)):
    await UserRepository.delete_all_users(db)
