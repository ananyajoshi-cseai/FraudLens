from datetime import datetime, timedelta, timezone
from pymongo.database import Database


def check_velocity(
    db: Database,
    user_id: str,
    window_minutes: int = 5,
    threshold: int = 3
) -> dict:

    now = datetime.now(timezone.utc)
    window_start = now - timedelta(minutes=window_minutes)

    count = db["transactions"].count_documents({
        "user_id": user_id,
        "timestamp": {
            "$gte": window_start,
            "$lte": now
        }
    })

    triggered = count >= threshold

    return {
        "count": count,
        "window_minutes": window_minutes,
        "threshold": threshold,
        "triggered": triggered,
        "impact": 20 if triggered else 0,
        "message": (
            f"{count} transactions were detected within "
            f"{window_minutes} minutes."
        )
    }