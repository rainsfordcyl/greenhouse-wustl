import time
import sensors
import actuators
import datalog

def check_soil_and_water_if_needed(
    sensor_id,
    valve_id,
    valve_open,
    time_valve_opened,
    dry_threshold=600,
    soak_seconds=2
):
    """
    1) Reads sensor.
    2) Logs sensor data.
    3) If dryness > threshold => turn valve ON for 'soak_seconds'.
    4) Otherwise ensure valve is OFF.
    5) Return updated (valve_open, time_valve_opened).
    """

    # Read the sensor
    sensors.set_mux_channel(sensor_id)
    raw_value = sensors.read_mcp3008(channel=0)

    if raw_value > dry_threshold: # Soil is dry
        if not valve_open:
            # print("Soil is dry -> open valve.")
            # open the valve
            actuators.valve_on(valve_id)
            datalog.log_actuator("open", valve_id)
            valve_open = True
            time_valve_opened = time.time()

            # wait for 2 seconds
            while (time.time() - time_valve_opened) < 2:
                pass

            # # problem: data stopped recording when waiting for watering
            # # wait until soil becomes wet
            # while True:
            #     sensors.set_mux_channel(sensor_id)
            #     raw_value = sensors.read_mcp3008(channel=0)
                
            #     if raw_value <= dry_threshold:
            #         break
            
            # close the valve
            elapsed = time.time() - time_valve_opened
            print(f"Soil is now wet -> closing valve (open for {elapsed:.1f}s).")
            actuators.valve_off()
            datalog.log_actuator("close", valve_id, elapsed)
            valve_open = False
            time_valve_opened = 0
            
    else: # Soil is wet
        if valve_open:
            duration = time.time() - time_valve_opened
            # print("Soil is wet -> close valve.")
            actuators.valve_off()

            datalog.log_actuator("close", valve_id, duration)
            valve_open = False
    return valve_open, time_valve_opened