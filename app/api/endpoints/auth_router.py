from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.core.services.auth_service import AuthService
from app.core.repositories.auth_repository import AuthRepository
from app.database import get_db

from app.api.models.token import Token

router = APIRouter(tags=['Authentication'])

# @router.post("/login", response_model=Token)
@router.post("/login")
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = await AuthRepository.get_user_by_email(db=db, email=user_credentials.username)

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')

    if not AuthService.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')

    # Create token
    access_token = AuthService.create_access_token(user)
    return {"access_token": access_token, "token_type": "bearer"}
