import psutil

print("=== Running Processes ===")

for proc in psutil.process_iter(['pid', 'name']):
    try:
        print(f"PID: {proc.info['pid']} | Name: {proc.info['name']}")
    except:
        pass