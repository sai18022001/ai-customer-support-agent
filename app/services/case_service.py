from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.case import Case
from app.core.exceptions import NotFoundError


class CaseService:
    def __init__(self, db: Session):
        self.db = db

    def get_case(self, case_id: str) -> Case:
        case = self.db.query(Case).filter(Case.id == case_id).first()
        if not case:
            raise NotFoundError("Case", case_id)
        return case

    def list_cases(
        self,
        customer_id: str | None = None,
        status: str | None = None,
        priority: str | None = None,
        category: str | None = None,
        page: int = 1,
        limit: int = 20,
    ) -> list[Case]:
        query = self.db.query(Case)
        if customer_id:
            query = query.filter(Case.customer_id == customer_id)
        if status:
            query = query.filter(Case.status == status)
        if priority:
            query = query.filter(Case.priority == priority)
        if category:
            query = query.filter(Case.category == category)
        offset = (page - 1) * limit
        return query.order_by(Case.created_at.desc()).offset(offset).limit(limit).all()

    def create_case(self, **kwargs) -> Case:
        case = Case(**kwargs)
        self.db.add(case)
        self.db.commit()
        self.db.refresh(case)
        return case

    def update_case(self, case_id: str, **kwargs) -> Case:
        case = self.get_case(case_id)
        for key, value in kwargs.items():
            if value is not None:
                setattr(case, key, value)
        if kwargs.get("status") == "resolved" and not case.resolved_at:
            case.resolved_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(case)
        return case

    def escalate_case(self, case_id: str, assigned_to: str) -> Case:
        return self.update_case(
            case_id,
            status="escalated",
            assigned_to=assigned_to,
        )
