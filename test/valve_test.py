import time
import RPi.GPIO as GPIO

# -----------------------------------------
# 1) Pin Assignments
# -----------------------------------------
# Four address pins for the 74154 demux
A = 5    # 74154 pin 23 to GPIO 5
B = 6    # 74154 pin 22
C = 13   # 74154 pin 21
D = 19   # 74154 pin 20

# -----------------------------------------
# 2) Setup GPIO
# -----------------------------------------
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

for pin in [A, B, C, D]:
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

# -----------------------------------------
# 3) Helper Function to Set Demux Channel
# -----------------------------------------
def set_demux_channel(channel):
    """
    channel: 0..15
    74154 is active-low. If channel=0 => Y0 is LOW, all others HIGH.
    """
    # Break 'channel' into 4 bits for A0..A3
    GPIO.output(A, channel & 0x01)
    GPIO.output(B, (channel >> 1) & 0x01)
    GPIO.output(C, (channel >> 2) & 0x01)
    GPIO.output(D, (channel >> 3) & 0x01)

# -----------------------------------------
# 4) Main Loop
# -----------------------------------------
try:
    while True:
        # Turn the valve ON by making Y0 LOW => set channel=0
        set_demux_channel(0)
        print("Valve OPEN")
        time.sleep(1)  # keep valve open for 1 second

        # Turn the valve OFF by selecting a different channel => Y0 goes HIGH
        # We'll choose channel=15 => Y15=LOW, so Y0=HIGH => valve off
        set_demux_channel(15)
        print("Valve CLOSED")
        time.sleep(1)  # valve is closed for 1 second

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
