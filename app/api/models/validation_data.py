from pydantic import BaseModel

class ValidationData(BaseModel):
    event_id: int
    reference: str
