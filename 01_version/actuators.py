import RPi.GPIO as GPIO

# Address pins for the CD74HC4067
S0 = 17
S1 = 27
S2 = 22
S3 = 23
SIG_PIN = 24

def init_actuators():
    """
    Sets up the MUX pins as outputs and permanently enables the chip
    by tying EN to GND physically.
    """
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    for pin in (S0, S1, S2, S3):
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
    
    GPIO.setup(SIG_PIN, GPIO.OUT, initial=GPIO.LOW)

def select(channel):
    """
    channel: 0..15
    The selected channel => SIG pin is connected to C[channel].
    All other C pins are disconnected.
    """
    GPIO.output(S0, channel & 0x01)
    GPIO.output(S1, (channel >> 1) & 0x01)
    GPIO.output(S2, (channel >> 2) & 0x01)
    GPIO.output(S3, (channel >> 3) & 0x01)

def turn_on(channel):
    select(channel)
    GPIO.output(SIG_PIN, GPIO.HIGH)

def turn_off(channel):
    select(channel)
    GPIO.output(SIG_PIN, GPIO.LOW)

def deactivate_all():
    """
    Turn SIG pin LOW and optionally select a 'dummy' channel (like 15) 
    that isn't used. This effectively leaves all real channels unpowered.
    """
    # Setting SIG=LOW ensures no channel sees a HIGH voltage.
    GPIO.output(SIG_PIN, GPIO.LOW)