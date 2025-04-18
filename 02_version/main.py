import time
import RPi.GPIO as GPIO
import sensors
import actuators
import datalog
import controller

def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    sensors.init_sensors()
    actuators.init_actuators()
    datalog.init_logs()

    try:
        while True:
            # Whenever a new MQTT message arrives:
            if sensors.has_new_data():
                sensor_id, percent_val = sensors.get_latest_reading()
                # Log the reading
                datalog.log_sensor(sensor_id, percent_val, percent_val)

                print(f"Sensor {sensor_id} : {percent_val:.2f}%")
                # Enqueue this sensor if it's below the dryness threshold
                controller.enqueue_if_dry(sensor_id, percent_val, dry_threshold=80, soak_seconds=2)

                # Now process the queue. If this sensor is new, it will get watered after any
                # currently-watering sensor finishes.
                controller.process_queue()

            # Brief sleep to avoid busy-loop
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("User interrupted. Exiting...")
    finally:
        actuators.turn_off_all()
        sensors.close_sensors()
        GPIO.cleanup()

if __name__ == "__main__":
    main()