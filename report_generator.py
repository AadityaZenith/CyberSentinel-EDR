import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional

import os

# Use repo-relative paths so the module works from any working directory.
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(REPO_ROOT, "database", "incidents.db")


def _severity_rank(sev: str) -> int:
    if not sev:
        return 0
    s = sev.strip().upper()
    return {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}.get(s, 0)


def fetch_incidents(
    *,
    pid: Optional[int] = None,
    process_name: Optional[str] = None,
    severity: Optional[str] = None,
    date_str: Optional[str] = None,
    db_path: str = DB_PATH,
) -> List[Dict[str, Any]]:
    """Fetch incident rows.

    NOTE: Current DB schema (by design, no DB changes):
      incidents(id, process_name, pid, threat_score, severity)

    Your requested filters include Date/Action/Timestamp fields, but since
    DB isn't updated yet, those will be treated as unavailable.

    - date_str filter is ignored (no date column)
    - action is returned as None
    - timestamp is returned as None
    """

    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        where = []
        params: List[Any] = []

        if pid is not None:
            where.append("pid = ?")
            params.append(pid)
        if process_name:
            where.append("process_name = ?")
            params.append(process_name)
        if severity:
            where.append("severity = ?")
            params.append(severity)

        # date_str ignored for now (no column in schema)

        sql = "SELECT id, process_name, pid, threat_score, severity FROM incidents"
        if where:
            sql += " WHERE " + " AND ".join(where)

        sql += " ORDER BY id DESC"
        cursor.execute(sql, params)
        rows = cursor.fetchall()

        incidents: List[Dict[str, Any]] = []
        for row in rows:
            _id, proc, _pid, score, sev = row
            incidents.append(
                {
                    "id": _id,
                    "pid": _pid,
                    "process": proc,
                    "severity": (sev or "").strip().upper() if sev else None,
                    "threat_score": score,
                    "timestamp": None,
                    "action": None,
                    "date": None,
                }
            )
        return incidents
    finally:
        conn.close()


def generate_text_report(
    *,
    report_date: Optional[datetime] = None,
    analyst_name: str = "Analyst",
    db_path: str = DB_PATH,
) -> str:
    """Generate a crisp text report.

    Since DB has no timestamp/date/action, this report uses:
      - Date: report_date if provided else 'N/A'
      - Killed processes: computed as 0 (no action column yet)
      - Timestamp: None

    Returns report text.
    """

    incidents = fetch_incidents(db_path=db_path)

    total_threats = len(incidents)
    # No action info in current DB
    killed_processes: List[Dict[str, Any]] = []

    date_label = (report_date.strftime("%d-%m-%Y") if report_date else "N/A")
    timestamp_label = "N/A"

    # Sort by severity then threat_score
    def sort_key(x: Dict[str, Any]):
        return (
            _severity_rank(x.get("severity") or ""),
            x.get("threat_score") or 0,
            x.get("pid") or 0,
        )

    incidents_sorted = sorted(incidents, key=sort_key, reverse=True)

    lines: List[str] = []
    lines.append("CyberSentinel EDR Report")
    lines.append(f"Date: {date_label}")
    lines.append(f"Total Threats: {total_threats}")
    lines.append("")

    lines.append("Threats:")
    lines.append("--------------------------------")
    for inc in incidents_sorted:
        lines.append(f"PID: {inc['pid']}")
        lines.append(f"Process: {inc['process']}")
        lines.append(f"Severity: {inc.get('severity')}")
        # Action unavailable
        lines.append(f"Action: {inc.get('action') or 'N/A'}")
        lines.append("")

    # Killed processes summary (not available yet)
    lines.append("Killed Processes:")
    if killed_processes:
        for inc in killed_processes:
            lines.append(f"- PID {inc['pid']} | {inc['process']} ({inc.get('severity')})")
    else:
        lines.append("- N/A (action column not yet in DB schema)")

    lines.append("")
    lines.append(f"Analyst Name: {analyst_name}")
    lines.append(f"Timestamp: {timestamp_label}")

    return "\n".join(lines)

