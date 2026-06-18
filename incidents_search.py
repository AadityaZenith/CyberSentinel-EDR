import sqlite3
from typing import Any, Dict, List, Optional

import os

# Use repo-relative paths so the module works from any working directory.
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(REPO_ROOT, "database", "incidents.db")


def search_incidents(
    *,
    pid: Optional[int] = None,
    process_name: Optional[str] = None,
    date_str: Optional[str] = None,
    severity: Optional[str] = None,
    db_path: str = DB_PATH,
) -> List[Dict[str, Any]]:
    """Search incidents by PID / process_name / severity.

    NOTE: DB currently has no date column, so date_str is ignored.
    Action and timestamp are also not available yet.
    """

    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
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

        # date_str ignored

        sql = "SELECT id, process_name, pid, threat_score, severity FROM incidents"
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += " ORDER BY id DESC"

        cur.execute(sql, params)
        rows = cur.fetchall()

        results: List[Dict[str, Any]] = []
        for _id, proc, _pid, score, sev in rows:
            results.append(
                {
                    "id": _id,
                    "pid": _pid,
                    "process": proc,
                    "severity": (sev or "").strip().upper() if sev else None,
                    "timestamp": None,
                    "date": None,
                    "action": None,
                    "threat_score": score,
                }
            )
        return results
    finally:
        conn.close()

