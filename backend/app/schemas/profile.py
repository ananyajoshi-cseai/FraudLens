from pydantic import BaseModel
from typing import List


class UserProfile(BaseModel):
    user_id: str
    usual_amount_avg: float
    usual_amount_max: float
    usual_transaction_hour_start: int
    usual_transaction_hour_end: int
    known_beneficiaries: List[str]
    known_devices: List[str]