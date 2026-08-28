from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from pymongo.database import Database

from app.schemas.transaction import TransactionRequest
from app.schemas.profile import UserProfile
from app.schemas.risk import RiskResponse, TransactionData

from app.services.risk_engine import calculate_risk
from app.services.explanation_engine import generate_explanations
from app.services.recommendation_engine import generate_recommendation
from app.services.velocity_engine import check_velocity
from app.core.database import get_db


router = APIRouter(
    prefix="/api/transactions",
    tags=["Transactions"]
)


@router.post("/analyze", response_model=RiskResponse)
def analyze_transaction(
    transaction: TransactionRequest,
    db: Database = Depends(get_db)
):

    # 1. Fetch user profile from MongoDB
    collection = db["profiles"]

    user_data = collection.find_one({
        "user_id": transaction.user_id
    })

    if not user_data:
        raise HTTPException(
            status_code=404,
            detail="User profile not found in database."
        )

    # Convert MongoDB document into Pydantic profile
    profile = UserProfile(**user_data)

    # 2. Calculate base risk
    risk_result = calculate_risk(
        transaction,
        profile
    )

    # 3. Check transaction velocity
    velocity_result = check_velocity(
        db,
        transaction.user_id
    )

    # 4. Add velocity impact to risk score
    if velocity_result["triggered"]:
        risk_result["risk_score"] += velocity_result["impact"]

    # Keep risk score between 0 and 100
    risk_result["risk_score"] = min(
        risk_result["risk_score"],
        100
    )

    # Recalculate risk level after velocity adjustment
    if risk_result["risk_score"] <= 30:
        risk_result["risk_level"] = "LOW"

    elif risk_result["risk_score"] <= 60:
        risk_result["risk_level"] = "MEDIUM"

    else:
        risk_result["risk_level"] = "HIGH"

    # Add velocity signal if triggered
    if velocity_result["triggered"]:
        risk_result["signals"].append({
            "signal": "velocity_anomaly",
            "impact": velocity_result["impact"],
            "message": velocity_result["message"]
        })

    # 5. Generate explanations
    reasons = generate_explanations(
        risk_result["signals"]
    )

    # 6. Generate recommendation
    recommended_action = generate_recommendation(
        risk_result["risk_level"],
        risk_result["signals"]
    )

    # 7. Save transaction to MongoDB
    transaction_data = {
        "user_id": transaction.user_id,
        "amount": transaction.amount,
        "beneficiary_id": transaction.beneficiary_id,
        "beneficiary_name": transaction.beneficiary_name,
        "transaction_hour": transaction.transaction_hour,
        "device_id": transaction.device_id,
        "failed_attempts": transaction.failed_attempts,
        "risk_score": risk_result["risk_score"],
        "risk_level": risk_result["risk_level"],
        "reasons": reasons,
        "recommended_action": recommended_action,
        "timestamp": datetime.now(timezone.utc)
    }

    db["transactions"].insert_one(transaction_data)

    # 8. Return final response
    return RiskResponse(
        transaction=TransactionData(
            user_id=transaction.user_id,
            amount=transaction.amount,
            beneficiary_id=transaction.beneficiary_id,
            beneficiary_name=transaction.beneficiary_name,
            transaction_hour=transaction.transaction_hour,
            device_id=transaction.device_id,
            failed_attempts=transaction.failed_attempts
        ),
        risk_score=risk_result["risk_score"],
        risk_level=risk_result["risk_level"],
        reasons=reasons,
        recommended_action=recommended_action
    )


@router.get("")
def get_all_transactions(
    db: Database = Depends(get_db)
):
    """
    Return all transactions for the dashboard
    and audit log screens.
    """

    transactions = list(
        db["transactions"]
        .find(
            {},
            {"_id": 0}
        )
        .sort("timestamp", -1)
    )

    return transactions


@router.get("/{user_id}")
def get_transaction_history(
    user_id: str,
    db: Database = Depends(get_db)
):
    """
    Return transaction history for a specific user.
    """

    transactions = list(
        db["transactions"]
        .find(
            {"user_id": user_id},
            {"_id": 0}
        )
        .sort("timestamp", -1)
    )

    return {
        "user_id": user_id,
        "count": len(transactions),
        "transactions": transactions
    }
