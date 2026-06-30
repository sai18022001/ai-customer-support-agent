from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import require_api_key
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse
from app.services.crm_service import CRMService

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("", response_model=list[OrderResponse])
def list_orders(
    customer_id: str | None = None,
    status: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _key: str = Depends(require_api_key),
):
    svc = CRMService(db)
    return svc.list_orders(customer_id=customer_id, status=status, page=page, limit=limit)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: str,
    db: Session = Depends(get_db),
    _key: str = Depends(require_api_key),
):
    svc = CRMService(db)
    return svc.get_order(order_id)


@router.post("", response_model=OrderResponse, status_code=201)
def create_order(
    body: OrderCreate,
    db: Session = Depends(get_db),
    _key: str = Depends(require_api_key),
):
    svc = CRMService(db)
    return svc.create_order(
        customer_id=body.customer_id,
        product_id=body.product_id,
        quantity=body.quantity,
    )


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: str,
    body: OrderUpdate,
    db: Session = Depends(get_db),
    _key: str = Depends(require_api_key),
):
    svc = CRMService(db)
    return svc.update_order(order_id, **body.model_dump(exclude_unset=True))
