import psutil

PROTECTED_PROCESSES = [
    "explorer.exe",
    "svchost.exe",
    "System",
    "MsMpEng.exe",
    "RuntimeBroker.exe"
]

pid = int(input("Enter PID to terminate: "))

try:
    process = psutil.Process(pid)
    name = process.name()

    print(f"Process Found: {name}")

    if name in PROTECTED_PROCESSES:
        print("Protected system process. Cannot terminate.")
        exit()

    confirm = input("Terminate? (y/n): ")

    if confirm.lower() == "y":
        process.kill()
        print("Process Terminated Successfully")
    else:
        print("Cancelled")

except Exception as e:
    print("Error:", e)