from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import require_api_key
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse
from app.services.crm_service import CRMService

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("", response_model=list[CustomerResponse])
def list_customers(
    tier: str | None = None,
    search: str | None = None,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    _auth: str = Depends(require_api_key),
):
    return CRMService(db).list_customers(
        tier=tier, search=search, page=page, limit=limit
    )


@router.get("/{cid}", response_model=CustomerResponse)
def get_customer(
    cid: str,
    db: Session = Depends(get_db),
    _auth: str = Depends(require_api_key),
):
    return CRMService(db).get_customer(cid)


@router.post("", response_model=CustomerResponse, status_code=201)
def create_customer(
    payload: CustomerCreate,
    db: Session = Depends(get_db),
    _auth: str = Depends(require_api_key),
):
    return CRMService(db).create_customer(**payload.model_dump())


@router.put("/{cid}", response_model=CustomerResponse)
def update_customer(
    cid: str,
    payload: CustomerUpdate,
    db: Session = Depends(get_db),
    _auth: str = Depends(require_api_key),
):
    return CRMService(db).update_customer(cid, **payload.model_dump(exclude_unset=True))
