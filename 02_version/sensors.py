import paho.mqtt.client as mqtt

latest_sensor_id = 0
latest_percent_val = 0.0
new_data_available = False

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker for sensor data.")
    client.subscribe("esp32/#")

def on_message(client, userdata, msg):
    global latest_sensor_id, latest_percent_val, new_data_available

    payload_str = msg.payload.decode('utf-8').strip()  # e.g. "2 35"
    try:
        parts = payload_str.split()
        if len(parts) != 2:
            print(f"Invalid sensor data: '{payload_str}' (need 'sensor_id percent_val')")
            return

        sensor_id_str, percent_str = parts
        sensor_id = int(sensor_id_str)
        percent_val = float(percent_str)

        # Update globals
        latest_sensor_id = sensor_id
        latest_percent_val = percent_val

        # Signal to main loop that new data just arrived
        new_data_available = True

        # print(f"Received: sensor_id={sensor_id}, percent={percent_val}%")

    except ValueError:
        print(f"Invalid sensor data received: {payload_str}")

def init_sensors():
    global client
    client = mqtt.Client("rpi_sensor_client")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("127.0.0.1", 1883)
    client.loop_start()

def has_new_data():
    """Return True if the last MQTT message was not yet processed by main.py."""
    return new_data_available

def get_latest_reading():
    """
    Return (sensor_id, percent_val) AND mark that data as 'consumed'.
    Main.py will call this once per new message.
    """
    global new_data_available
    new_data_available = False
    return (latest_sensor_id, latest_percent_val)

def close_sensors():
    global client
    client.loop_stop()
    client.disconnect()