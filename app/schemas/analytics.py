from pydantic import BaseModel


class OverviewMetrics(BaseModel):
    total_sessions: int
    ai_resolved: int
    escalated: int
    resolution_rate: float
    avg_response_time_ms: float
    avg_satisfaction: float
    active_sessions: int


class IntentCount(BaseModel):
    intent: str
    count: int
    percentage: float


class IntentDistribution(BaseModel):
    intents: list[IntentCount]


class DailyTrend(BaseModel):
    date: str
    sessions: int
    resolved: int
    escalated: int


class TrendsResponse(BaseModel):
    period: str
    data: list[DailyTrend]
