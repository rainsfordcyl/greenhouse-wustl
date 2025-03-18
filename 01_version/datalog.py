#!/usr/bin/env python3
import csv
import os
from datetime import datetime

DATA_DIR = "data"

SENSOR_LOG_FILE = os.path.join(DATA_DIR, "sensor_log.csv")
ACTUATOR_LOG_FILE = os.path.join(DATA_DIR, "actuator_log.csv")

"""
key: valve_id, value: float (accumulated seconds)
Dictionary to track how many seconds each valve was open "today"
"""
daily_usage = {}
current_date = datetime.now().strftime("%Y-%m-%d")

def init_logs():
    """
    If the CSV log files don't exist, create them with headers.
    Also create the data/ folder if it doesn't exist.
    """
    if not os.path.isdir(DATA_DIR):
        os.makedirs(DATA_DIR)

    # Sensor log: date/time, sensor#, raw value, percentage
    if not os.path.exists(SENSOR_LOG_FILE):
        with open(SENSOR_LOG_FILE, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["datetime", "sensor_id", "raw_value", "percent_value"])

    # Actuator log: date/time, event_type, valve_id, duration_seconds, daily_total
    if not os.path.exists(ACTUATOR_LOG_FILE):
        with open(ACTUATOR_LOG_FILE, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["datetime", "event_type", "valve_id", "duration_seconds", "daily_total"])

def log_sensor_reading(sensor_id, raw_value, percent_value):
    """
    Appends a row to sensor_log.csv with:
      - current date/time
      - sensor_id
      - raw_value (0..1023)
      - percent_value (0..100)
    """
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(SENSOR_LOG_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([now_str, sensor_id, raw_value, f"{percent_value:.2f}"])

def log_actuator_event(event_type, valve_id, duration_seconds=None):
    """
    Appends a row to actuator_log.csv with:
      - datetime
      - event_type (e.g. "open", "close")
      - valve_id
      - duration_seconds (float, optional)
      - daily_total (float) how many seconds the valve was open today

    If event_type == "close" and duration_seconds is provided,
    we add that duration to the daily total for 'valve_id'.
    At midnight, we reset all daily totals to 0.
    """
    global current_date, daily_usage

    now = datetime.now()
    now_date = now.strftime("%Y-%m-%d")
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")

    # Check if the date changed (i.e., past midnight)
    if now_date != current_date:
        # Reset daily usage for all valves
        daily_usage.clear()
        current_date = now_date

    # If it's a "close" event with a duration, add it to today's total
    if event_type == "close" and duration_seconds is not None:
        old_total = daily_usage.get(valve_id, 0.0)
        new_total = old_total + duration_seconds
        daily_usage[valve_id] = new_total
        daily_valve_time = new_total
    else:
        # For "open" events or no duration, daily total is unchanged
        daily_valve_time = daily_usage.get(valve_id, 0.0)

    # Write to CSV
    with open(ACTUATOR_LOG_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            now_str,
            event_type,
            valve_id,
            f"{duration_seconds:.2f}" if duration_seconds else "",
            f"{daily_valve_time:.2f}"
        ])