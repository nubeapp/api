from app import utils

class UserService:
    @staticmethod
    async def hashed_password(plain_password):
        return utils.hash(plain_password)
