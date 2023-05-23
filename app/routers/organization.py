from typing import List

from ..models import OrganizationRequest, OrganizationResponse
from .. import schemas
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi import status, Depends, APIRouter
from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/organizations",
    tags=['Organization']
)

@router.get("", response_model=List[OrganizationResponse])
async def get_organizations(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    organizations = db.query(schemas.Organization).all()
    return organizations

@router.post("", status_code=status.HTTP_201_CREATED, response_model=OrganizationResponse)
async def create_organization(organization: OrganizationRequest, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    new_organization = schemas.Organization(**organization.dict())
    db.add(new_organization)
    db.commit()
    db.refresh(new_organization)
    return new_organization