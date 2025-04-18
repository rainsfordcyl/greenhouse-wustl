import json
import time
import threading

from flask import Flask, Response, render_template, send_file
import sensors
import datalog

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sensor-updates")
def sensor_updates():
    """
    Server-Sent Events endpoint: streams JSON whenever new data is available
    in sensors.py.
    """
    def event_stream():
        while True:
            if sensors.has_new_data():
                readings = sensors.get_all_readings_and_reset()
                json_str = json.dumps(readings)
                yield f"data: {json_str}\n\n"
            time.sleep(0.1)

    return Response(event_stream(), mimetype="text/event-stream")


@app.route("/download-sensor-history")
def download_sensor_history():
    """
    Sends the sensor_log.csv file to the client as a download.
    """
    return send_file(datalog.SENSOR_FILE, as_attachment=True)


def run_flask():
    app.run(host="100.70.55.93", port=5000, debug=False)

if __name__ == "__main__":
    sensors.init_sensors()
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")

    finally:
        sensors.close_sensors()