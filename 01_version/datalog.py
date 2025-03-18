import csv
import os
from datetime import datetime

DATA_DIR = "data"
SENSOR_FILE = os.path.join(DATA_DIR, "sensor_log.csv")
ACTUATOR_FILE = os.path.join(DATA_DIR, "actuator_log.csv")

# For tracking daily usage
_daily_usage = {}
_current_date = datetime.now().strftime("%Y-%m-%d")

def init_logs():
    """Create CSV files with headers if they do not exist."""
    if not os.path.isdir(DATA_DIR):
        os.makedirs(DATA_DIR)

    if not os.path.exists(SENSOR_FILE):
        with open(SENSOR_FILE, 'w', newline='') as f:
            csv.writer(f).writerow(["datetime", "sensor_id", "raw_value", "percent"])

    if not os.path.exists(ACTUATOR_FILE):
        with open(ACTUATOR_FILE, 'w', newline='') as f:
            csv.writer(f).writerow(["datetime", "event", "valve_id", "duration_sec", "daily_total_sec"])

def log_sensor(sensor_id, raw_val, percent_val):
    """Append a row (timestamp, sensor_id, raw, percent)."""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(SENSOR_FILE, 'a', newline='') as f:
        csv.writer(f).writerow([now_str, sensor_id, raw_val, f"{percent_val:.2f}"])

def log_actuator(event_type, valve_id, duration_seconds=None):
    """
    Log an actuator event: "open" or "close".
    If event_type == "close", we add 'duration_seconds' to daily usage.
    """
    global _daily_usage, _current_date

    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    today_str = now.strftime("%Y-%m-%d")

    # Reset daily usage if date changed
    if today_str != _current_date:
        _daily_usage.clear()
        _current_date = today_str

    daily_total = _daily_usage.get(valve_id, 0.0)
    if event_type == "close" and duration_seconds:
        daily_total += duration_seconds
        _daily_usage[valve_id] = daily_total

    with open(ACTUATOR_FILE, 'a', newline='') as f:
        csv.writer(f).writerow([
            now_str,
            event_type,
            valve_id,
            f"{duration_seconds:.2f}" if duration_seconds else "",
            f"{daily_total:.2f}"
        ])