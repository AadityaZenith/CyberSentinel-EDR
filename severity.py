from typing import Optional


LEVELS = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]


def classify_severity(
    *,
    process_name: str,
    threat_score: Optional[int] = None,
) -> str:
    """Classify severity without changing DB schema.

    Current DB already stores severity, but this module can be used by other
    teams for consistent mapping.

    Rules (simple & deterministic):
      - Known names override
      - Else use threat_score bands (if provided)
      - Else default LOW
    """

    pname = (process_name or "").lower().strip()

    # Overrides from your requirement
    if pname == "malware.exe":
        return "CRITICAL"
    if pname == "powershell.exe":
        return "MEDIUM"

    if threat_score is None:
        # fall back to LOW if nothing is known
        return "LOW"

    try:
        score = int(threat_score)
    except Exception:
        return "LOW"

    if score >= 80:
        return "CRITICAL"
    if score >= 50:
        return "HIGH"
    if score >= 20:
        return "MEDIUM"
    return "LOW"

