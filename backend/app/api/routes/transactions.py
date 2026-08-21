from fastapi import APIRouter

from app.schemas.transaction import TransactionRequest
from app.schemas.profile import UserProfile
from app.schemas.risk import RiskResponse

from app.services.risk_engine import calculate_risk
from app.services.explanation_engine import generate_explanations
from app.services.recommendation_engine import generate_recommendation


router = APIRouter(
    prefix="/api/transactions",
    tags=["Transactions"]
)


@router.post("/analyze", response_model=RiskResponse)
def analyze_transaction(transaction: TransactionRequest):

    # Temporary demo profile.
    # This will later come from MongoDB.
    profile = UserProfile(
        user_id=transaction.user_id,
        usual_amount_avg=1200,
        usual_amount_max=5000,
        usual_transaction_hour_start=8,
        usual_transaction_hour_end=22,
        known_beneficiaries=["B101", "B205", "B310"],
        known_devices=["DEV-OLD-01"]
    )

    # 1. Calculate risk
    risk_result = calculate_risk(
        transaction,
        profile
    )

    # 2. Generate explanations
    reasons = generate_explanations(
        risk_result["signals"]
    )

    # 3. Generate recommendation
    recommended_action = generate_recommendation(
        risk_result["risk_level"],
        risk_result["signals"]
    )

    # 4. Return final response
    return RiskResponse(
        risk_score=risk_result["risk_score"],
        risk_level=risk_result["risk_level"],
        reasons=reasons,
        recommended_action=recommended_action
    )