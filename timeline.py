from typing import Any, Dict, List


def build_threat_timeline(*, incident: Dict[str, Any]) -> List[str]:
    """Build a timeline for an incident.

    NOTE: With current DB schema (no timestamps/events), this returns a
    placeholder sequence for forensic display.

    If later the DB is extended with event timestamps, this function can be
    updated to order by those fields.
    """

    process_name = incident.get("process") or incident.get("process_name")
    return [
        f"Detected -> {process_name} (timestamp not available)",
        f"Hash generated -> {process_name} (timestamp not available)",
        f"Process terminated -> {process_name} (timestamp not available)",
    ]

