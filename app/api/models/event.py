from datetime import datetime
from pydantic import BaseModel

from app.api.models.organization import OrganizationResponse

class EventBase(BaseModel):
    title: str
    date: datetime
    time: str
    venue: str    

    class Config:
        orm_mode = True

class EventRequest(EventBase):
    organization_id: int

    class Config:
        orm_mode = True

class EventResponse(EventBase):
    id: int
    # created_at: datetime
    organization: OrganizationResponse

    class Config:
        orm_mode = True
