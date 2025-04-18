import time
import RPi.GPIO as GPIO
import sensors
import actuators

def test_sensor():
    try:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        sensors.init_sensors()

        print("Reading MCP3008 channel 0 raw values. Press Ctrl+C to stop.")
        while True:
            raw_val = sensors.read_mcp3008(channel=0)  # or whichever channel you want
            print(f"Raw ADC Value: {raw_val}")
            time.sleep(1.0)
    except KeyboardInterrupt:
        pass
    finally:
        sensors.close_sensors()


SIG_PIN = 24

def test_actuators():
    try:
        actuators.init_actuators()        

        while(True):
            # actuators.turn_on(0)            # select 0 ch
            # GPIO.output(SIG_PIN, GPIO.HIGH) # turn 0 ch to HIGH
            # time.sleep(1)
            # GPIO.output(SIG_PIN, GPIO.LOW)  # turn 0 ch to LOW
            # time.sleep(1)

            # actuators.turn_on(1)            # select 1 ch
            # GPIO.output(SIG_PIN, GPIO.HIGH) # turn 1 ch to HIGH
            # time.sleep(4)                   # 0 ch shouldn't be HIGH here

            actuators.turn_on(2)
            # time.sleep(1)
            # actuators.turn_off(0)
            # time.sleep(1)

            # actuators.turn_on(1)        # select 1 ch
            # GPIO.output(SIG, GPIO.HIGH) # turn 1 ch to HIGH
            # time.sleep(2)


    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    # test_sensor()
    test_actuators()