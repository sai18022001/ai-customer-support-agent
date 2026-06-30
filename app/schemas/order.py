from datetime import datetime

from pydantic import BaseModel


class OrderCreate(BaseModel):
    customer_id: str
    product_id: str
    quantity: int = 1


class OrderUpdate(BaseModel):
    status: str | None = None
    quantity: int | None = None


class OrderResponse(BaseModel):
    id: str
    customer_id: str
    product_id: str
    quantity: int
    total_amount: float
    status: str
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}
