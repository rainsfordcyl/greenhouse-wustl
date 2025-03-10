import RPi.GPIO as GPIO

# ----- 74154 DEMUX PIN ASSIGNMENTS -----
A = 5   # Pin 23 on the 74154
B = 6   # Pin 22
C = 13  # Pin 21
D = 19  # Pin 20

def init_actuators():
    """
    Set up the 74154 demux pins as outputs, initial LOW.
    Call this once at startup.
    """
    for pin in (A, B, C, D):
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

def set_demux_channel(channel):
    """
    channel: 0..15
    If channel=0 => Y0 is LOW => relay on that output active (for an active-low relay).
    """
    GPIO.output(A, channel & 0x01)
    GPIO.output(B, (channel >> 1) & 0x01)
    GPIO.output(C, (channel >> 2) & 0x01)
    GPIO.output(D, (channel >> 3) & 0x01)

def valve_on():
    """
    Example: Turn ON valve at Y0. 
    Adjust if you have multiple valves on different Y outputs.
    """
    set_demux_channel(0)

def valve_off():
    """
    Example: Turn OFF valve at Y0 by selecting a channel that isn't 0 
    (like 15, making Y15=LOW and Y0=HIGH).
    """
    set_demux_channel(15)
