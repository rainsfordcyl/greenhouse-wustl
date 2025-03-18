import time
import RPi.GPIO as GPIO
import sensors
import actuators
import datalog
import controller

def main():
    try:
        # Initialize
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        sensors.init_sensors()
        actuators.init_actuators()
        datalog.init_logs()

        valve_open = False
        valve_open_time = 0

        # We'll read sensor_id=0, control valve_id=0
        while True:
            valve_open, valve_open_time = controller.monitor_soil_and_control_valve(
                sensor_id=0,
                valve_id=0,
                valve_open=valve_open,
                valve_open_time=valve_open_time,
                dry_threshold=600
            )
            time.sleep(3)  # Delay between checks

    except KeyboardInterrupt:
        pass
    finally:
        # If valve is on at exit, log final close
        if valve_open:
            duration = time.time() - valve_open_time
            datalog.log_actuator_event("close", valve_id=0, duration_seconds=duration)
            actuators.valve_off()

        sensors.close_sensors()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
