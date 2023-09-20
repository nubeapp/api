from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
# from app.core.services.validation_service import ValidationService
from app.dependencies import get_db
from app.models.validation_data import ValidationData
from app.oauth2 import get_current_user
from app.decorators import validate_ticket_history
from fastapi import status

router = APIRouter(prefix="/validation", tags=['Validation'])

@router.put("", status_code=status.HTTP_200_OK)
@validate_ticket_history
async def validate_ticket(validation_data: ValidationData, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return {"message": "ticket validated successfully"}

