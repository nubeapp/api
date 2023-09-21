from sqlalchemy.orm import Session
from typing import List
from app.api.models.organization import OrganizationRequest, OrganizationResponse
from app.core.repositories.organization_repository import OrganizationRepository

class OrganizationService:
    @staticmethod
    async def get_organizations(db: Session) -> List[OrganizationResponse]:
        return await OrganizationRepository.get_organizations(db)

    @staticmethod
    async def get_organization_by_id(db: Session, id: int) -> OrganizationResponse:
        return await OrganizationRepository.get_organization_by_id(db, id)
    
    @staticmethod
    async def get_organization_by_name(db: Session, name: str) -> OrganizationResponse:
        return await OrganizationRepository.get_organization_by_name(db, name)

    @staticmethod
    async def create_organization(db: Session, organization: OrganizationRequest) -> OrganizationResponse:
        return await OrganizationRepository.create_organization(db, organization)

    @staticmethod
    async def delete_organization_by_id(db: Session, id: int) -> None:
        await OrganizationRepository.delete_organization_by_id(db, id)

    @staticmethod
    async def delete_all_organizations(db: Session) -> None:
        await OrganizationRepository.delete_all_organizations(db)
