from app.schemas.user import User
from app import utils, oauth2

class AuthService:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return utils.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(user: User):
        return oauth2.create_access_token(data={"user_id": user.id})
