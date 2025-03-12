#!/usr/bin/env python3
import RPi.GPIO as GPIO
import spidev
import time

MUX_S0 = 17
MUX_S1 = 27
MUX_S2 = 22
MUX_S3 = 23

sensor_channels = [0, 1, 2]
sensor_data = {}  # e.g., {0: {"raw":0, "percent":0.0}, ...}

spi = spidev.SpiDev()

def setup_sensors():
    # GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    for pin in (MUX_S0, MUX_S1, MUX_S2, MUX_S3):
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

    # SPI
    spi.open(0, 0)
    spi.max_speed_hz = 1350000

    for ch in sensor_channels:
        sensor_data[ch] = {"raw": 0, "percent": 0.0}

def set_mux_channel(channel):
    GPIO.output(MUX_S0, channel & 0x01)
    GPIO.output(MUX_S1, (channel >> 1) & 0x01)
    GPIO.output(MUX_S2, (channel >> 2) & 0x01)
    GPIO.output(MUX_S3, (channel >> 3) & 0x01)

def read_mcp3008(adc_channel=0):
    cmd1 = 1
    cmd2 = (8 + adc_channel) << 4
    adc_response = spi.xfer2([cmd1, cmd2, 0])
    raw_val = ((adc_response[1] & 3) << 8) | adc_response[2]
    return raw_val

def update_sensor_readings():
    for mux_ch in sensor_channels:
        set_mux_channel(mux_ch)
        time.sleep(0.01)
        raw_val = read_mcp3008(0)
        percent_val = (raw_val / 1023) * 100
        sensor_data[mux_ch]["raw"] = raw_val
        sensor_data[mux_ch]["percent"] = round(percent_val, 1)

def cleanup_sensors():
    spi.close()
    GPIO.cleanup()
