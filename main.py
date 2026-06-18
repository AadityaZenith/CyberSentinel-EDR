import sqlite3
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(title="CyberSentinel EDR API")

# Allow communication between frontend and backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "database/incidents.db"

class KillRequest(BaseModel):
    pid: int

@app.get("/api/processes")
def get_processes():
    # Safety fallback if Aaditya's engine hasn't created the database file yet
    if not os.path.exists(DB_PATH):
        return [
            {"pid": "18200", "name": "CalculatorApp.exe", "offset": "0x000472b6", "status": "Suspicious"},
            {"pid": "4324", "name": "chrome.exe", "offset": "0x001a4b2c", "status": "Verified"},
            {"pid": "9840", "name": "unknown_script.py", "offset": "0x000f81a1", "status": "Suspicious"}
        ]
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT pid, process_name, threat_score, severity FROM incidents")
        rows = cursor.fetchall()
        
        process_list = []
        for row in rows:
            status = "Suspicious" if row[2] > 50 or row[3] in ["High", "Medium"] else "Verified"
            process_list.append({
                "pid": str(row[0]),
                "name": row[1],
                "offset": f"0x{row[0]:08x}",
                "status": status
            })
        return process_list if process_list else [{"pid": "18200", "name": "CalculatorApp.exe", "offset": "0x000472b6", "status": "Suspicious"}]
    except sqlite3.OperationalError:
        return [{"pid": "18200", "name": "CalculatorApp.exe", "offset": "0x000472b6", "status": "Suspicious"}]
    finally:
        conn.close()

@app.post("/api/kill-process")
def kill_process(req: KillRequest):
    try:
        import psutil
        p = psutil.Process(req.pid)
        p.terminate()
        return {"status": "success", "message": f"Process {req.pid} has been terminated from memory."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Serves your frontend interface directly from the dashboard folder
app.mount("/", StaticFiles(directory="dashboard", html=True), name="dashboard")