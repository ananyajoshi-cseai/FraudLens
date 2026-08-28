from app.schemas.transaction import TransactionRequest
from app.schemas.profile import UserProfile


def calculate_risk(
    transaction: TransactionRequest,
    profile: UserProfile,
    velocity_result: dict | None = None
) -> dict:

    score = 0
    signals = []

    # 1. Amount anomaly
    if transaction.amount > profile.usual_amount_max:
        score += 25
        signals.append({
            "signal": "amount_anomaly",
            "impact": 25,
            "message": (
                f"This transaction amount of ₹{transaction.amount:.0f} "
                f"is higher than the user's usual maximum of "
                f"₹{profile.usual_amount_max:.0f}."
            )
        })

    # 2. New beneficiary
    if transaction.beneficiary_id not in profile.known_beneficiaries:
        score += 20
        signals.append({
            "signal": "new_beneficiary",
            "impact": 20,
            "message": (
                "This beneficiary has not been previously associated "
                "with this user's transaction history."
            )
        })

    # 3. Unusual transaction time
    if not (
        profile.usual_transaction_hour_start
        <= transaction.transaction_hour
        <= profile.usual_transaction_hour_end
    ):
        score += 15
        signals.append({
            "signal": "unusual_time",
            "impact": 15,
            "message": (
                "This transaction is being made outside the user's "
                "usual transaction hours."
            )
        })

    # 4. New device
    if transaction.device_id not in profile.known_devices:
        score += 20
        signals.append({
            "signal": "new_device",
            "impact": 20,
            "message": (
                "This transaction was initiated from a device "
                "not previously associated with the user."
            )
        })

    # 5. Failed attempts
    if transaction.failed_attempts >= 2:
        score += 15
        signals.append({
            "signal": "failed_attempts",
            "impact": 15,
            "message": (
                f"{transaction.failed_attempts} failed attempts "
                "were recorded before this transaction."
            )
        })

    # 6. Transaction velocity
    if velocity_result and velocity_result["triggered"]:
        score += 10
        signals.append({
            "signal": "transaction_velocity",
            "impact": 10,
            "message": (
                f"This user has made "
                f"{velocity_result['count']} transactions within "
                f"{velocity_result['window_minutes']} minutes."
            )
        })

    # Keep score within 0–100
    score = min(score, 100)

    # Risk classification
    if score <= 30:
        risk_level = "LOW"
    elif score <= 60:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"

    return {
        "risk_score": score,
        "risk_level": risk_level,
        "signals": signals
    }