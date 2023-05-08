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

class UserRequest(UserBase):
    password: str

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

class CodeRequest(CodeBase):
    pass

class CodeResponse(CodeBase):
    created_at: datetime

    class Config:
        orm_mode = True

# endregion

# region EmailData

class EmailDataBase(BaseModel):
    email: EmailStr
    name: str
    code: str

class EmailDataRequest(EmailDataBase):
    pass

class EmailDataResponse(EmailDataBase):
    pass

# endregion

# region Organization

class OrganizationBase(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class OrganizationRequest(OrganizationBase):
    pass

class OrganizationResponse(OrganizationBase):
    pass
# endregion

# region Event

class EventBase(BaseModel):
    title: str
    date: datetime
    time: str
    venue: str    

    class Config:
        orm_mode = True

class EventRequest(EventBase):
    ticket_limit: int
    ticket_available: int
    organization_id: int

    class Config:
        orm_mode = True

class EventResponse(EventBase):
    id: int
    created_at: datetime
    organization: OrganizationRequest

    class Config:
        orm_mode = True

# endregion

# region Ticket

class TicketBase(BaseModel):
    reference: str
    price: float 

    class Config:
        orm_mode = True

class TicketRequest(TicketBase):
    event_id: int

class TicketResponse(TicketBase):
    id: int
    event: EventResponse

    class Config:
        orm_mode = True

# endregion

# region Assistant

class AssistantBase(BaseModel):
    ticket_id: int

    class Config:
        orm_mode = True

class AssistantRequest(AssistantBase):
    pass

class AssistantResponse(AssistantBase):
    ticket: TicketResponse

    class Config:
        orm_mode = True

# endregion

class AssistantTicketResponse(BaseModel):
    user: UserResponse
    ticket: TicketResponse

    class Config:
        orm_mode = True