from sqlalchemy.orm import Session
from typing import List
from app.api.models.organization import OrganizationRequest, OrganizationResponse
from app.schemas.organization import Organization

class OrganizationRepository:
    @staticmethod
    async def get_organizations(db: Session) -> List[OrganizationResponse]:
        organizations = db.query(Organization).all()
        return organizations

    @staticmethod
    async def get_organization_by_id(db: Session, id: int) -> OrganizationResponse:
        organization = db.query(Organization).filter(Organization.id == id).first()
        return organization
    
    @staticmethod
    async def get_organization_by_name(db: Session, name: str) -> OrganizationResponse:
        organization = db.query(Organization).filter(Organization.name == name).first()
        return organization

    @staticmethod
    async def create_organization(db: Session, organization: OrganizationRequest) -> OrganizationResponse:
        new_organization = Organization(**organization.dict())
        db.add(new_organization)
        db.commit()
        db.refresh(new_organization)
        return new_organization

    @staticmethod
    async def delete_organization_by_id(db: Session, id: int) -> None:
        organization = db.query(Organization).filter(Organization.id == id).first()
        if organization:
            db.delete(organization)
            db.commit()

    @staticmethod
    async def delete_all_organizations(db: Session) -> None:
        db.query(Organization).delete()
        db.commit()
