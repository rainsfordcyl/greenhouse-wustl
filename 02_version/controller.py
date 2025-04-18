import time
import datalog
import actuators
from collections import deque

# Global FIFO queue holding (sensor_id, soak_seconds)
_water_queue = deque()

def is_in_queue(sensor_id):
    """
    Returns True if 'sensor_id' is already in _water_queue.
    """
    return any(item[0] == sensor_id for item in _water_queue)

def enqueue_if_dry(sensor_id, current_percent, dry_threshold, soak_seconds=2):
    """
    If current_percent < dry_threshold => queue this sensor for watering,
    but only if it's not already in the queue.

    After adding the new sensor, print the entire queue (just the sensor_ids)
    in order, separated by spaces. E.g. "1 2 3"
    """
    # ### for debugging purposes:
    # if sensor_id != 2:
    #     return
    # ###

    if current_percent < dry_threshold:
        if not is_in_queue(sensor_id):
            _water_queue.append((sensor_id, soak_seconds))
            # Build a list of sensor_ids currently in the queue
            sensor_list = [str(item[0]) for item in _water_queue]
            # Print them all in one line
            print(" ".join(sensor_list))

def process_queue():
    """
    Sequentially waters each sensor in the queue:
      1) Turn on that sensor's valve
      2) Busy-wait for soak_seconds
      3) Turn off all valves (demux limitation)
      4) Remove that sensor from the queue
    """
    while _water_queue:
        sensor_id, soak_seconds = _water_queue[0]  # Peek at the first item

        # 1) Turn on that sensor's valve
        actuators.turn_on(sensor_id)
        datalog.log_actuator("open", sensor_id)
        start_time = time.time()

        # 2) Busy-wait for soak_seconds
        while (time.time() - start_time) < soak_seconds:
            pass

        # 3) Turn off all valves
        elapsed = time.time() - start_time
        actuators.turn_off_all()
        datalog.log_actuator("close", sensor_id, elapsed)

        # 4) Remove the sensor from the queue
        _water_queue.popleft()