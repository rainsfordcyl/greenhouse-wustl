import time
import RPi.GPIO as GPIO
import sensors
import actuators

WET_THRESHOLD = 600

def main():
    try:
        # 1) INIT GPIO
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        sensors.init_sensors()
        actuators.init_actuators()

        while True:
            # Read sensor from MUX channel 0, MCP3008 CH0
            sensors.set_mux_channel(0)
            raw_value = sensors.read_mcp3008(channel=0)
            voltage = (raw_value * 3.3) / 1023.0
            print(f"[Sensor] raw={raw_value} voltage={voltage:.3f}")

            # Decide to water or not
            if raw_value < WET_THRESHOLD:
                print("Soil is dry -> valve ON for 2 seconds.")
                actuators.valve_on()
                time.sleep(2)
                print("Valve OFF.")
                actuators.valve_off()
            else:
                print("Soil is wet enough -> keep valve OFF.")
                actuators.valve_off()

            print("---")
            time.sleep(3)  # wait a bit before next read

    except KeyboardInterrupt:
        pass
    finally:
        sensors.close_sensors()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
