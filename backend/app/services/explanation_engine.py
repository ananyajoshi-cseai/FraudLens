def generate_explanations(signals: list[dict]) -> list[dict]:
    """
    Convert detected risk signals into user-friendly explanations.
    """

    explanations = []

    for signal in signals:
        explanations.append({
            "signal": signal["signal"],
            "impact": signal["impact"],
            "message": signal["message"]
        })

    return explanations