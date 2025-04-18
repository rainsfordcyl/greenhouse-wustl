# sensors.py
import paho.mqtt.client as mqtt
import datalog

# Dictionary: key = sensor ID, value = float reading
sensor_data = {}
new_data_available = False
client = None

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker.")
    client.subscribe("esp32/#")

def on_message(client, userdata, msg):
    global new_data_available
    payload_str = msg.payload.decode("utf-8").strip()  # e.g. "0 44.7"
    parts = payload_str.split()
    if len(parts) == 2:
        try:
            sensor_id = int(parts[0])
            sensor_val = float(parts[1])
            sensor_data[sensor_id] = sensor_val
            new_data_available = True
            print(f"[MQTT] Sensor {sensor_id}: {sensor_val}")
            datalog.log_sensor_reading(sensor_id, sensor_val)
        except ValueError:
            print(f"Invalid sensor data: {payload_str}")
    else:
        print(f"Invalid format: {payload_str}")

def init_sensors():
    global client
    datalog.init_logs()
    client = mqtt.Client("rpi_sensor_client")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("127.0.0.1", 1883)
    client.loop_start()

def has_new_data():
    return new_data_available

def get_all_readings_and_reset():
    """Return a copy of sensor_data and reset the 'new_data_available' flag."""
    global new_data_available
    new_data_available = False
    # Return a shallow copy so we don't expose the original dictionary externally.
    return dict(sensor_data)

def close_sensors():
    global client
    client.loop_stop()
    client.disconnect()