import sqlite3

conn = sqlite3.connect("database/incidents.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM incidents")

rows = cursor.fetchall()

print("\n=== INCIDENT LOGS ===\n")

for row in rows:
    print(row)

conn.close()