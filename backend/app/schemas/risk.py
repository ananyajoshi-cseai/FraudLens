from pydantic import BaseModel
from typing import List


class RiskReason(BaseModel):
    signal: str
    impact: int
    message: str


class TransactionData(BaseModel):
    user_id: str
    amount: float
    beneficiary_id: str
    beneficiary_name: str
    transaction_hour: int
    device_id: str
    failed_attempts: int


class RiskResponse(BaseModel):
    transaction: TransactionData
    risk_score: int
    risk_level: str
    reasons: List[RiskReason]
    recommended_action: str