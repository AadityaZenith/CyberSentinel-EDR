import psutil
import sqlite3
import time
from threat_rules import SAFE_PROCESSES, SUSPICIOUS_PROCESSES

print("CyberSentinel EDR Started...")

while True:

    conn = sqlite3.connect("database/incidents.db")
    cursor = conn.cursor()

    print("\nScanning...")

    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        try:

            process_name = proc.info['name']

            # Skip trusted processes
            if process_name in SAFE_PROCESSES:
                continue

            score = 0

            # Check known suspicious process names
            if process_name in SUSPICIOUS_PROCESSES:
                score += 80

            # High Memory Usage
            if proc.info['memory_percent'] > 5:
                score += 20

            # High CPU Usage
            cpu = proc.cpu_percent(interval=0.1)

            if cpu > 50:
                score += 30

            # Skip if not suspicious
            if score == 0:
                continue

            # Severity Level
            if score >= 80:
                severity = "Critical"
            elif score >= 50:
                severity = "High"
            elif score >= 20:
                severity = "Medium"
            else:
                severity = "Low"

            # Save Incident
            cursor.execute("""
            INSERT INTO incidents
            (process_name, pid, threat_score, severity)
            VALUES (?, ?, ?, ?)
            """,
            (
                process_name,
                proc.info['pid'],
                score,
                severity
            ))

            print(
                f"[{severity}] "
                f"{process_name} | "
                f"PID={proc.info['pid']} | "
                f"Score={score}"
            )

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):
            pass

    conn.commit()
    conn.close()

    time.sleep(10)