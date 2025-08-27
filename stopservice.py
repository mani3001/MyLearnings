import subprocess

def stop_printer_service():
    try:
        # Print Spooler service name in Windows is "Spooler"
        subprocess.run(["sc", "start", "Spooler"], check=True, shell=True)
        print("Printer service (Spooler) stopped successfully.")
    except subprocess.CalledProcessError as e:
        print("Failed to stop printer service:", e)

if __name__ == "__main__":
    stop_printer_service()