from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import require_api_key
from app.core.exceptions import NotFoundError
from app.models.session import ChatSession
from app.models.message import Message
from app.schemas.chat import ChatRequest, ChatResult, ActionInfo, ChatSessionDetail, ChatMessageItem
from app.services.ai_engine import ai_engine
from app.services.crm_service import CRMService
from app.services.action_executor import ActionExecutor

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResult)
def send_message(
    body: ChatRequest,
    db: Session = Depends(get_db),
    _auth: str = Depends(require_api_key),
):
    crm = CRMService(db)
    crm.get_customer(body.customer_id)

    if body.session_id:
        chat_session = db.query(ChatSession).filter(ChatSession.id == body.session_id).first()
        if not chat_session:
            raise NotFoundError("Session", body.session_id)
    else:
        chat_session = ChatSession(customer_id=body.customer_id)
        db.add(chat_session)
        db.commit()
        db.refresh(chat_session)

    customer_msg = Message(
        session_id=chat_session.id,
        role="customer",
        content=body.message,
    )

    classification = ai_engine.classify_message(body.message)

    customer_msg.intent = classification.get("intent", "general")
    customer_msg.sentiment = classification.get("sentiment", "neutral")
    customer_msg.confidence = classification.get("confidence", 0.5)
    db.add(customer_msg)
    db.commit()

    executor = ActionExecutor(db, chat_session.id)
    executed = []
    for action_name in classification.get("suggested_actions", []):
        params = {"customer_id": body.customer_id}
        result = executor.execute(action_name, params)
        executed.append(ActionInfo(action_type=result["action_type"], status=result["status"]))

    prev_messages = (
        db.query(Message)
        .filter(Message.session_id == chat_session.id)
        .order_by(Message.created_at)
        .all()
    )
    history = [{"role": m.role, "content": m.content} for m in prev_messages]

    customer_context = crm.get_customer_summary(body.customer_id)

    reply_text = ai_engine.generate_response(
        message=body.message,
        customer_context=customer_context,
        conversation_history=history,
        classification=classification,
    )

    agent_msg = Message(
        session_id=chat_session.id,
        role="agent",
        content=reply_text,
    )
    db.add(agent_msg)

    was_escalated = classification.get("requires_escalation", False)
    if was_escalated:
        chat_session.escalated = True
        chat_session.status = "escalated"

    db.commit()

    return ChatResult(
        session_id=chat_session.id,
        reply=reply_text,
        detected_intent=classification.get("intent", "general"),
        detected_sentiment=classification.get("sentiment", "neutral"),
        confidence_score=classification.get("confidence", 0.5),
        executed_actions=executed,
        was_escalated=was_escalated,
    )


@router.get("/sessions/{sid}", response_model=ChatSessionDetail)
def get_session(
    sid: str,
    db: Session = Depends(get_db),
    _auth: str = Depends(require_api_key),
):
    chat_session = db.query(ChatSession).filter(ChatSession.id == sid).first()
    if not chat_session:
        raise NotFoundError("Session", sid)

    msgs = (
        db.query(Message)
        .filter(Message.session_id == sid)
        .order_by(Message.created_at)
        .all()
    )

    return ChatSessionDetail(
        session_id=chat_session.id,
        customer_id=chat_session.customer_id,
        status=chat_session.status,
        conversation=[
            ChatMessageItem(
                id=m.id,
                role=m.role,
                content=m.content,
                intent=m.intent,
                sentiment=m.sentiment,
                created_at=m.created_at,
            )
            for m in msgs
        ],
        started_at=chat_session.started_at,
    )
