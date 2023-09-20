from pydantic import BaseModel, EmailStr

class EmailDataBase(BaseModel):
    email: EmailStr
    name: str
    code: str

class EmailDataRequest(EmailDataBase):
    pass

class EmailDataResponse(EmailDataBase):
    pass
