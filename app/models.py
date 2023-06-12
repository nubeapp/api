from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from typing import List
from enum import Enum

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
    name: str

    class Config:
        orm_mode = True

class OrganizationRequest(OrganizationBase):
    pass

class OrganizationResponse(OrganizationBase):
    id: int
    # created_at: datetime

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
    organization_id: int

    class Config:
        orm_mode = True

class EventResponse(EventBase):
    id: int
    # created_at: datetime
    organization: OrganizationResponse

    class Config:
        orm_mode = True

# endregion

# region Ticket

class TicketStatus(Enum):
    AVAILABLE = 'AVAILABLE'
    SOLD = 'SOLD'
    CANCELED = 'CANCELED'

class TicketBase(BaseModel):
    reference: str
    price: float 
    status: Optional[TicketStatus] = TicketStatus.AVAILABLE

    class Config:
        orm_mode = True

class TicketRequest(TicketBase):
    event_id: int
    order_id: Optional[int] = None
    user_id: Optional[int] = None

class TicketResponse(TicketBase):
    id: int
    # created_at: datetime
    # event: EventResponse

    class Config:
        orm_mode = True

class TicketSummary(BaseModel):
    event: EventResponse
    tickets: List[TicketResponse]

    class Config:
        orm_mode = True

class CreateTicket(BaseModel):
    event_id: int
    price: float
    limit: int

# endregion

# region Order

class OrderBase(BaseModel):
    pass

class OrderRequest(OrderBase):
    event_id: int
    quantity: int

class OrderResponse(OrderBase):
    id: int
    created_at: datetime
    tickets: List[TicketResponse]

    class Config:
        orm_mode = True

# endregion