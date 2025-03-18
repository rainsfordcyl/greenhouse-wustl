import time
import RPi.GPIO as GPIO
import sensors
import actuators
import datalog
import controller

def main():
    # Setup
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    sensors.init_sensors()
    actuators.init_actuators()
    datalog.init_logs()

    LOG_INTERVAL = 1            # seconds -> sensor logging
    WATER_CHECK_INTERVAL = 10    # seconds -> 10 minutes
    last_watering_check = 0
    last_data_log = 0

    valve_open = False
    time_valve_opened = 0

    try:
        while True:
            now = time.time()
            # read and record data every LOG_INTERVAL seconds
            if now - last_data_log >= LOG_INTERVAL:
                sensors.set_mux_channel(0)
                raw_value = sensors.read_mcp3008(0)
                percent_val = (raw_value / 1023.0) * 100.0
                datalog.log_sensor(0, raw_value, percent_val)

                actuator_state = "OPEN" if valve_open else "CLOSED"
                print(f"Sensor reading: raw={raw_value}, percent={percent_val:.2f}%, valve is {actuator_state}")

                last_data_log = now

            # check watering every WATER_CHECK_INTERVAL seconds
            if now - last_watering_check >= WATER_CHECK_INTERVAL:
                valve_open, time_valve_opened = controller.check_soil_and_water_if_needed(
                    sensor_id=0,
                    valve_id=0,
                    valve_open=valve_open,
                    time_valve_opened=time_valve_opened,
                    dry_threshold=600,   # dryness threshold
                    soak_seconds=2       # water for 2 seconds
                )
                last_watering_check = now

    except KeyboardInterrupt:
        print("User interrupted. Exiting...")
    finally:
        if valve_open:
            duration = time.time() - time_valve_opened
            actuators.valve_off()
            datalog.log_actuator("close", 0, duration)

        sensors.close_sensors()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
