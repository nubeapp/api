# from typing import List

# from ..models import OrganizationRequest, OrganizationResponse
# from .. import schemas
# from sqlalchemy.orm import Session
# from ..database import get_db
# from fastapi import HTTPException, status, Depends, APIRouter
# from app.oauth2 import get_current_user

# router = APIRouter(
#     prefix="/organizations",
#     tags=['Organization']
# )

# @router.get("", response_model=List[OrganizationResponse])
# async def get_organizations(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
#     organizations = db.query(schemas.Organization).all()
#     return organizations

# @router.get("/{id}", response_model=OrganizationResponse)
# async def get_organization_by_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
#     organization = db.query(schemas.Organization).filter(schemas.Organization.id == id).first()
#     return organization

# @router.post("", status_code=status.HTTP_201_CREATED, response_model=OrganizationResponse)
# async def create_organization(organization: OrganizationRequest, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
#     new_organization = schemas.Organization(**organization.dict())
#     db.add(new_organization)
#     db.commit()
#     db.refresh(new_organization)
#     return new_organization

# @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_organization_by_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
#     organization = db.query(schemas.Organization).filter(schemas.Organization.id == id).first()
#     if not organization:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No organization found for id {id}")
#     db.delete(organization)
#     db.commit()

# @router.delete("", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_all_organizations(db: Session = Depends(get_db)):
#     db.query(schemas.Organization).delete()
#     db.commit()