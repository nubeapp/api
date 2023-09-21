from fastapi import APIRouter
from app.api.models.email_data import EmailDataRequest
from app.core.services.email_service import EmailService

router = APIRouter(
    prefix="/email",
    tags=['Email']
)

@router.post("/send")
async def send_code(email_data: EmailDataRequest):
    response = EmailService.send_email(email_data)
    return response
