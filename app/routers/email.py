import requests
from fastapi import APIRouter, Request

from ..models import EmailData


router = APIRouter(
    prefix="/email",
    tags=['Email']
)

URL = 'https://api.emailjs.com/api/v1.0/email/send'
SERVICE_ID = 'service_4juazb9'
TEMPLATE_ID = 'template_ovslkk6'
PUBLIC_KEY = 'm6_PyyRTyKWUZmEUA'
PRIVATE_KEY = 'ZIyAmgPSEegPkyc5Wg_5x'

@router.post("/send")
async def send_code(email_data: EmailData):
    email = email_data.email
    name = email_data.name
    code = email_data.code
    headers = {'Content-Type': 'application/json'}
    template_params = {
        'user_email': email,
        'name': name,
        'verification_code': code,
    }
    data = {
        'service_id': SERVICE_ID,
        'template_id': TEMPLATE_ID,
        'user_id': PUBLIC_KEY,
        'accessToken': PRIVATE_KEY,
        'template_params': template_params,
    }
    try:
        response = requests.post(URL, headers=headers, json=data)
        response.raise_for_status()
        return {"message": "Email sent successfully"}
    except requests.exceptions.RequestException as e:
        return {"message": f"Error sending email: {e}"}
    