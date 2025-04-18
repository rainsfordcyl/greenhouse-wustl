import os
import csv
from datetime import datetime

DATA_DIR = "data"
SENSOR_FILE = os.path.join(DATA_DIR, "sensor_log.csv")

def init_logs():
    """
    Create the data folder (if missing) and a CSV file with headers (if missing).
    """
    if not os.path.isdir(DATA_DIR):
        os.makedirs(DATA_DIR)

    if not os.path.exists(SENSOR_FILE):
        with open(SENSOR_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "sensor_id", "reading"])

def log_sensor_reading(sensor_id, reading):
    """
    Append a row to sensor_log.csv: (timestamp, sensor_id, reading).
    """
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(SENSOR_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([now_str, sensor_id, f"{reading:.2f}"])
