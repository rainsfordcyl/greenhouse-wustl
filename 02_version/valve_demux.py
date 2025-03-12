#!/usr/bin/env python3
import RPi.GPIO as GPIO

# 74154 pin assignments (address lines)
A = 5
B = 6
C = 13
D = 19

# Suppose you have valves on Y0..Y3
valve_channels = [0, 1, 2, 3]

# Track on/off states of each valve channel
valve_states = {}

def setup_demux():
    """
    Initialize GPIO pins for the 74154 demultiplexer (valves).
    Also sets all valves to OFF by default.
    """
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # Setup address pins
    for pin in (A, B, C, D):
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

    # Initialize states as all OFF
    for ch in valve_channels:
        valve_states[ch] = False

    # Turn everything OFF by selecting channel=15 => Y15=LOW => Y0..Y14=HIGH
    set_demux_channel(15)

def set_demux_channel(channel):
    """
    The 74154 is active-low. Setting channel=X drives Y(X) = LOW, others = HIGH.
    If channel=15 => Y15=LOW => Y0..Y14=HIGH => effectively off for your normal valves.
    """
    GPIO.output(A, channel & 0x01)
    GPIO.output(B, (channel >> 1) & 0x01)
    GPIO.output(C, (channel >> 2) & 0x01)
    GPIO.output(D, (channel >> 3) & 0x01)

def valve_on(channel):
    """
    Turn ON the valve on the specified demux channel.
    """
    valve_states[channel] = True
    set_demux_channel(channel)

def valve_off(channel):
    """
    Turn OFF the valve by selecting channel=15, so the chosen valve returns to HIGH.
    """
    valve_states[channel] = False
    set_demux_channel(15)

def cleanup_demux():
    """
    Optional function to cleanup GPIO if needed on exit.
    """
    GPIO.cleanup()