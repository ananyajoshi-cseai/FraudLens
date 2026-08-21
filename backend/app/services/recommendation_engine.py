def generate_recommendation(
    risk_level: str,
    signals: list[dict]
) -> str:

    if risk_level == "HIGH":
        return "Block Transaction"

    if risk_level == "MEDIUM":
        return "Verify Beneficiary"

    return "Proceed Normally"