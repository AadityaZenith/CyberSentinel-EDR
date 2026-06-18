import csv
import sqlite3
from typing import Optional

import os

# Use repo-relative paths so the module works from any working directory.
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(REPO_ROOT, "database", "incidents.db")
OUT_PATH = os.path.join(REPO_ROOT, "reports", "incidents.csv")


def export_incidents_csv(*, out_path: str = OUT_PATH, db_path: str = DB_PATH) -> None:
    """Export incidents to CSV.

    NOTE: DB currently has no timestamp/action/date columns. CSV will still
    include those headers, filled with 'N/A'.
    """

    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        cur.execute("SELECT pid, process_name, severity FROM incidents ORDER BY id DESC")
        rows = cur.fetchall()

        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["PID", "Process", "Severity", "Timestamp", "Action"])
            for pid, process_name, severity in rows:
                writer.writerow(
                    [
                        pid,
                        process_name,
                        (severity or "").strip().upper() if severity else "",
                        "N/A",
                        "N/A",
                    ]
                )
    finally:
        conn.close()


if __name__ == "__main__":
    export_incidents_csv()

