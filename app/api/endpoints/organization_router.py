from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.oauth2 import get_current_user
from app.models.organization import OrganizationRequest, OrganizationResponse
from app.core.services.organization_service import OrganizationService

router = APIRouter(
    prefix="/organizations",
    tags=['Organization']
)

@router.get("", response_model=List[OrganizationResponse])
async def get_organizations(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    organizations = await OrganizationService.get_organizations(db)
    return organizations

@router.get("/{id}", response_model=OrganizationResponse)
async def get_organization_by_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    organization = await OrganizationService.get_organization_by_id(db, id)
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The organization with id {id} does not exist")
    return organization

@router.get("/name/{name}", response_model=OrganizationResponse)
async def get_organization_by_name(name: str, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    organization = await OrganizationService.get_organization_by_name(db, name)
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The organization with name {name} does not exist")
    return organization

@router.post("", status_code=status.HTTP_201_CREATED, response_model=OrganizationResponse)
async def create_organization(organization: OrganizationRequest, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    organization_db = await OrganizationService.get_organization_by_name(db, organization.name)
    if organization_db:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"The organization with name '{organization.name}' already exists")
    new_organization = await OrganizationService.create_organization(db, organization)
    return new_organization

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization_by_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    await OrganizationService.delete_organization_by_id(db, id)
    return {"message": f"Organization with ID {id} has been deleted"}

@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_organizations(db: Session = Depends(get_db)):
    await OrganizationService.delete_all_organizations(db)
    return {"message": "All organizations have been deleted"}
