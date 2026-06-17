import sqlite3

conn = sqlite3.connect("database/incidents.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS incidents(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    process_name TEXT,
    pid INTEGER,
    threat_score INTEGER,
    severity TEXT
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")