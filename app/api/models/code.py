from datetime import datetime
from pydantic import BaseModel, EmailStr

class CodeBase(BaseModel):
    email: EmailStr
    code: str

    class Config:
        orm_mode = True

class CodeRequest(CodeBase):
    pass

class CodeResponse(CodeBase):
    created_at: datetime

    class Config:
        orm_mode = True
