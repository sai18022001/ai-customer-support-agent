from datetime import datetime

from pydantic import BaseModel, EmailStr


class CustomerCreate(BaseModel):
    name: str
    email: str
    phone: str | None = None
    tier: str = "basic"
    company: str | None = None


class CustomerUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    tier: str | None = None
    company: str | None = None


class CustomerResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: str | None
    tier: str
    company: str | None
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}
