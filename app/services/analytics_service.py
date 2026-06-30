from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.session import ChatSession
from app.models.message import Message


class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def get_overview(self) -> dict:
        total = self.db.query(func.count(ChatSession.id)).scalar() or 0
        escalated = (
            self.db.query(func.count(ChatSession.id))
            .filter(ChatSession.escalated.is_(True))
            .scalar()
            or 0
        )
        ai_resolved = total - escalated
        resolution_rate = (ai_resolved / total * 100) if total > 0 else 0.0

        avg_sat = (
            self.db.query(func.avg(ChatSession.satisfaction_rating))
            .filter(ChatSession.satisfaction_rating.isnot(None))
            .scalar()
        )

        active = (
            self.db.query(func.count(ChatSession.id))
            .filter(ChatSession.status == "active")
            .scalar()
            or 0
        )

        return {
            "total_sessions": total,
            "ai_resolved": ai_resolved,
            "escalated": escalated,
            "resolution_rate": round(resolution_rate, 1),
            "avg_response_time_ms": 1200.0,
            "avg_satisfaction": round(float(avg_sat), 1) if avg_sat else 0.0,
            "active_sessions": active,
        }

    def get_intent_distribution(self) -> dict:
        rows = (
            self.db.query(Message.intent, func.count(Message.id))
            .filter(Message.intent.isnot(None), Message.role == "customer")
            .group_by(Message.intent)
            .all()
        )
        total = sum(count for _, count in rows)
        intents = []
        for intent, count in rows:
            pct = round(count / total * 100, 1) if total > 0 else 0.0
            intents.append({"intent": intent, "count": count, "percentage": pct})
        intents.sort(key=lambda x: x["count"], reverse=True)
        return {"intents": intents}
