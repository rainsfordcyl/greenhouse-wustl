#!/usr/bin/env python3
from flask import Flask, render_template, redirect, url_for, jsonify
import valve_demux
import sensor_mux

app = Flask(__name__)

@app.route('/')
def index():
    """
    Show the main page with valve states,
    but do NOT load sensor data here. We'll fetch it via JS.
    """
    return render_template('index.html',
                           valves=valve_demux.valve_states)

@app.route('/api/sensors')
def api_sensors():
    """
    Return the current sensor readings as JSON
    e.g. { "0": { "raw": 512 }, "1": { "raw": 300 }, ... }
    """
    sensor_mux.update_sensor_readings()
    return jsonify(sensor_mux.sensor_data)

@app.route('/toggle/<int:ch>')
def toggle_valve(ch):
    """
    Toggle a specific valve on channel 'ch'.
    """
    current_state = valve_demux.valve_states[ch]
    if current_state:
        valve_demux.valve_off(ch)
    else:
        valve_demux.valve_on(ch)
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Setup demux for valves
    valve_demux.setup_demux()
    # Setup sensor MUX + MCP3008
    sensor_mux.setup_sensors()

    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        pass
    finally:
        valve_demux.cleanup_demux()
        sensor_mux.cleanup_sensors()