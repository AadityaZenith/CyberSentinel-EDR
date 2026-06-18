import sqlite3

import os

# Use repo-relative paths so the module works from any working directory.
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(REPO_ROOT, "database", "incidents.db")


def cleanup_old_logs(*, days: int = 30, db_path: str = DB_PATH) -> None:
    """Auto cleanup old logs.

    NOTE: Current DB schema has no date/timestamp column, so this operation
    cannot be performed yet. This function is intentionally a no-op with a
    clear message.
    """

    raise NotImplementedError(
        "DB schema has no date/timestamp column for cleanup. "
        "When incidents table is extended, implement: "
        "DELETE FROM incidents WHERE date < 30 days."
    )

