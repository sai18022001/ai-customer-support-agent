from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import require_api_key
from app.schemas.analytics import OverviewMetrics, IntentDistribution
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/overview", response_model=OverviewMetrics)
def get_overview(
    db: Session = Depends(get_db),
    _auth: str = Depends(require_api_key),
):
    return AnalyticsService(db).get_overview()


@router.get("/intents", response_model=IntentDistribution)
def get_intents(
    db: Session = Depends(get_db),
    _auth: str = Depends(require_api_key),
):
    return AnalyticsService(db).get_intent_distribution()
