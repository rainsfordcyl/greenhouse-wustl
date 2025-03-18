import time
import sensors
import actuators
import datalog

DRY_THRESHOLD = 600

def monitor_soil_and_control_valve(
    sensor_id,
    valve_id,
    valve_open,
    valve_open_time,
    dry_threshold = DRY_THRESHOLD
):
    """
    1) Reads sensor from MUX + MCP3008
    2) Logs sensor reading
    3) Decides if the soil is dry/wet
    4) Toggles the valve on/off + logs actuator usage
    5) Returns (valve_open, valve_open_time)

    sensor_id: which MUX channel (and thus which sensor)
    valve_id: which 74154 channel or logic identifies the valve
    valve_open: boolean indicating if the valve is currently powered, if valve is powered on, it's watering
    valve_open_time: when the valve was last opened (for computing durations)
    dry_threshold: threshold for dryness check, above this is dry, below this is wet.
    """
    # --- (A) Read sensor ---
    sensors.set_mux_channel(sensor_id)
    raw_value = sensors.read_mcp3008(channel=0) # smaller means wetter, greater mean dryer
    voltage = (raw_value * 3.3) / 1023.0
    percent_val = (raw_value / 1023.0) * 100.0

    print(f"[Sensor #{sensor_id}] raw={raw_value}, voltage={voltage:.3f}")
    datalog.log_sensor_reading(sensor_id, raw_value, percent_val)

    # --- (B) Decide Watering Action ---
    if raw_value > dry_threshold: # dry
        if not valve_open:
            print("Soil is dry -> valve ON.")
            valve_open = True
            valve_open_time = time.time()
            actuators.valve_on()
            datalog.log_actuator_event("open", valve_id) # Log 'open'
        time.sleep(2) # Keep valve on for 2 seconds before next check

    else: # wet
        if valve_open:
            duration = time.time() - valve_open_time
            valve_open = False
            print("Soil is wet -> turning valve OFF.")
            actuators.valve_off()
            datalog.log_actuator_event("close", valve_id, duration_seconds=duration) # Log 'close'
        else:
            print("Soil is wet enough -> keep valve OFF.")

    print("---")
    return valve_open, valve_open_time
