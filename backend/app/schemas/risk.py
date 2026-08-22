from pydantic import BaseModel
from typing import List


class RiskReason(BaseModel):
    signal: str
    impact: int
    message: str


class RiskResponse(BaseModel):
    risk_score: int
    risk_level: str
    reasons: List[RiskReason]
    recommended_action: str