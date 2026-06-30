from datetime import datetime
from pydantic import BaseModel


class ChatRequest(BaseModel):
    customer_id: str
    message: str
    session_id: str | None = None


class ActionInfo(BaseModel):
    action_type: str
    status: str


class ChatResult(BaseModel):
    session_id: str
    reply: str
    detected_intent: str
    detected_sentiment: str
    confidence_score: float
    executed_actions: list[ActionInfo]
    was_escalated: bool


class ChatMessageItem(BaseModel):
    id: str
    role: str
    content: str
    intent: str | None
    sentiment: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class ChatSessionDetail(BaseModel):
    session_id: str
    customer_id: str
    status: str
    conversation: list[ChatMessageItem]
    started_at: datetime
