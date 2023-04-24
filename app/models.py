from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint

# region Users

class UserBase(BaseModel):
    email: EmailStr
    name: str
    surname: str

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    password: str
    profile_image: Optional[str] = None

    class Config:
        orm_mode = True

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# class UserLogin(UserBase):
#     email: EmailStr
#     password: str

#     class Config:
#         orm_mode = True

# endregion

# region Tokens

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

# endregion

# region Code

class CodeBase(BaseModel):
    email: EmailStr
    code: str

    class Config:
        orm_mode = True


class CodeResponse(CodeBase):
    created_at: datetime

    class Config:
        orm_mode = True

# endregion

# region EmailData

class EmailData(BaseModel):
    email: EmailStr
    name: str
    code: str

# endregion

# region Event

class EventBase(BaseModel):
    title: str
    completed: Optional[bool] = False

    class Config:
        orm_mode = True

class EventResponse(EventBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserBase

    class Config:
        orm_mode = True

# endregion

# region Assistant

class AssistantBase(BaseModel):
    event_id: int
    dir: conint(ge=0, le=1)

    class Config:
        orm_mode = True

# endregion