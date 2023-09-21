from pydantic import BaseModel

class OrganizationBase(BaseModel):
    name: str

    class Config:
        orm_mode = True

class OrganizationRequest(OrganizationBase):
    pass

class OrganizationResponse(OrganizationBase):
    id: int
