import requests
from app.config import settings
from app.models.email_data import EmailDataRequest

class EmailService:
    @staticmethod
    def send_email(email_data: EmailDataRequest):
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
            'service_id': settings.service_id,
            'template_id': settings.template_id,
            'user_id': settings.public_key,
            'accessToken': settings.private_key,
            'template_params': template_params,
        }
        try:
            response = requests.post(settings.url, headers=headers, json=data)
            response.raise_for_status()
            return {"message": "Email sent successfully"}
        except requests.exceptions.RequestException as e:
            return {"message": f"Error sending email: {e}"}
