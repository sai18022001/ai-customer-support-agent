import json
import logging

from sqlalchemy.orm import Session

from app.models.action import Action
from app.services.crm_service import CRMService
from app.services.case_service import CaseService

logger = logging.getLogger(__name__)


class ActionExecutor:
    def __init__(self, db: Session, session_id: str):
        self.db = db
        self.session_id = session_id
        self.crm = CRMService(db)
        self.case_svc = CaseService(db)

    def execute(self, action_type: str, params: dict | None = None) -> dict:
        """Execute a single action and record it in the database."""
        action = Action(
            session_id=self.session_id,
            action_type=action_type,
            parameters=json.dumps(params) if params else None,
        )
        self.db.add(action)

        handler = {
            "lookup_customer": self._lookup_customer,
            "lookup_order": self._lookup_order,
            "create_case": self._create_case,
            "update_account": self._update_account,
            "escalate_to_human": self._escalate,
        }.get(action_type)

        if handler is None:
            action.status = "failed"
            action.result = json.dumps({"detail": f"Unknown action: {action_type}"})
            self.db.commit()
            return {"action_type": action_type, "status": "failed"}

        try:
            result = handler(params or {})
            action.status = "completed"
            action.result = json.dumps(result)
            self.db.commit()
            return {"action_type": action_type, "status": "completed"}
        except Exception as exc:
            logger.warning("Action %s failed: %s", action_type, exc)
            action.status = "failed"
            action.result = json.dumps({"detail": str(exc)})
            self.db.commit()
            return {"action_type": action_type, "status": "failed"}

    def _lookup_customer(self, params: dict) -> dict:
        customer_id = params.get("customer_id", "")
        return self.crm.get_customer_summary(customer_id)

    def _lookup_order(self, params: dict) -> dict:
        order_id = params.get("order_id", "")
        order = self.crm.get_order(order_id)
        return {
            "order_id": order.id,
            "status": order.status,
            "total_amount": order.total_amount,
            "quantity": order.quantity,
        }

    def _create_case(self, params: dict) -> dict:
        case = self.case_svc.create_case(
            customer_id=params.get("customer_id", ""),
            subject=params.get("subject", "Support request"),
            description=params.get("description", "Auto-created by AI agent"),
            category=params.get("category", "general"),
        )
        return {"case_id": case.id, "status": case.status}

    def _update_account(self, params: dict) -> dict:
        customer_id = params.get("customer_id", "")
        updates = {k: v for k, v in params.items() if k != "customer_id"}
        customer = self.crm.update_customer(customer_id, **updates)
        return {"customer_id": customer.id, "updated_fields": list(updates.keys())}

    def _escalate(self, params: dict) -> dict:
        return {
            "escalated": True,
            "reason": params.get("reason", "Customer requested human agent"),
        }
