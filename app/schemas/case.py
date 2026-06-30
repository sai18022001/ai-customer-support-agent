from datetime import datetime

from pydantic import BaseModel


class CaseCreate(BaseModel):
    customer_id: str
    subject: str
    description: str
    priority: str = "medium"
    category: str | None = None


class CaseUpdate(BaseModel):
    status: str | None = None
    priority: str | None = None
    assigned_to: str | None = None
    resolution: str | None = None


class CaseResponse(BaseModel):
    id: str
    customer_id: str
    subject: str
    description: str
    status: str
    priority: str
    category: str | None
    assigned_to: str | None
    resolution: str | None
    created_at: datetime
    resolved_at: datetime | None
    updated_at: datetime | None

    model_config = {"from_attributes": True}
