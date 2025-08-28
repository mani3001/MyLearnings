import psutil
import time

def top_cpu_processes(limit=5, sample_interval=1.0, min_cpu=0.1):
    """
    Show top `limit` CPU-consuming processes.
    - sample_interval: seconds to wait while measuring CPU usage.
    - min_cpu: ignore processes with CPU < min_cpu (to skip tiny noise).
    """
    exclude_name_tokens = ("system idle process", "idle")  # filter names containing these
    # 1) Prime CPU counters
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            proc.cpu_percent(interval=None)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    # 2) Wait to get a meaningful sample
    time.sleep(sample_interval)

    # 3) Collect measurements, filtering out idle/system
    measured = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            info = proc.info
            pid = info.get('pid')
            name = (info.get('name') or "").strip()
            lname = name.lower()

            # Exclude System Idle Process by PID (0) and by name token
            if pid == 0:
                continue
            if any(token in lname for token in exclude_name_tokens):
                continue

            cpu = proc.cpu_percent(interval=None)
            if cpu >= min_cpu:
                measured.append({'pid': pid, 'name': name, 'cpu': cpu})
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # 4) Sort and display
    measured.sort(key=lambda x: x['cpu'], reverse=True)
    print(f"Top {limit} CPU-consuming processes (excluding System Idle):")
    for p in measured[:limit]:
        print(f"PID={p['pid']:<6} CPU%={p['cpu']:6.2f}  Name={p['name']}")

if __name__ == "__main__":
    # Example: top 5, 1 second sample interval
    top_cpu_processes(limit=5, sample_interval=1.0, min_cpu=0.1)
