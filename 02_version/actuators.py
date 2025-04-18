import RPi.GPIO as GPIO

# Address pins for the CD74HC4067 (demultiplexer)
S0 = 17
S1 = 27
S2 = 22
S3 = 23

# This pin is the "SIG" pin that provides HIGH or LOW output
SIG_PIN = 24

def init_actuators():
    """
    Sets up the demux pins as outputs and permanently enables the chip
    by tying EN to GND physically.
    """
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    for pin in (S0, S1, S2, S3):
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
    
    GPIO.setup(SIG_PIN, GPIO.OUT, initial=GPIO.LOW)

def _select_channel(channel):
    """
    Internal helper: set S0..S3 to select 'channel' (0..15).
    """
    GPIO.output(S0, channel & 0x01)
    GPIO.output(S1, (channel >> 1) & 0x01)
    GPIO.output(S2, (channel >> 2) & 0x01)
    GPIO.output(S3, (channel >> 3) & 0x01)

def turn_on(channel):
    """
    Turn on a single valve (channel).
    Because we have only one SIG pin, this will drive that single channel HIGH.
    """
    _select_channel(channel)
    GPIO.output(SIG_PIN, GPIO.HIGH)

def turn_off_all():
    """
    We cannot turn off a single channel individually.
    We can only drive SIG_PIN LOW, turning off all channels at once.
    """
    GPIO.output(SIG_PIN, GPIO.LOW)
    # Optional: select a 'dummy' channel if you like, e.g. channel 15
    _select_channel(15)