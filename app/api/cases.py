from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import require_api_key
from app.schemas.case import CaseCreate, CaseUpdate, CaseResponse
from app.services.case_service import CaseService

router = APIRouter(prefix="/cases", tags=["Cases"])


@router.get("", response_model=list[CaseResponse])
def list_cases(
    customer_id: str | None = None,
    status: str | None = None,
    priority: str | None = None,
    category: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _key: str = Depends(require_api_key),
):
    svc = CaseService(db)
    return svc.list_cases(
        customer_id=customer_id,
        status=status,
        priority=priority,
        category=category,
        page=page,
        limit=limit,
    )


@router.get("/{case_id}", response_model=CaseResponse)
def get_case(
    case_id: str,
    db: Session = Depends(get_db),
    _key: str = Depends(require_api_key),
):
    svc = CaseService(db)
    return svc.get_case(case_id)


@router.post("", response_model=CaseResponse, status_code=201)
def create_case(
    body: CaseCreate,
    db: Session = Depends(get_db),
    _key: str = Depends(require_api_key),
):
    svc = CaseService(db)
    return svc.create_case(**body.model_dump())


@router.put("/{case_id}", response_model=CaseResponse)
def update_case(
    case_id: str,
    body: CaseUpdate,
    db: Session = Depends(get_db),
    _key: str = Depends(require_api_key),
):
    svc = CaseService(db)
    return svc.update_case(case_id, **body.model_dump(exclude_unset=True))
