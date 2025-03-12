import spidev
import RPi.GPIO as GPIO

# ----- MUX PIN ASSIGNMENTS -----
MUX_S0 = 17
MUX_S1 = 27
MUX_S2 = 22
MUX_S3 = 23

# Create the SPI object at module level so you only open it once
spi = spidev.SpiDev()

def init_sensors():
    """
    Set up GPIO for the MUX and SPI for the MCP3008.
    Call this from your main script once at startup.
    """
    # Set MUX pins as outputs, initial LOW
    for pin in (MUX_S0, MUX_S1, MUX_S2, MUX_S3):
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

    # Initialize SPI
    spi.open(0, 0)              
    spi.max_speed_hz = 1350000  

def set_mux_channel(channel):
    """
    Select which MUX channel (0..15) to connect to the MCP3008 CH0.
    """
    GPIO.output(MUX_S0, channel & 0x01)
    GPIO.output(MUX_S1, (channel >> 1) & 0x01)
    GPIO.output(MUX_S2, (channel >> 2) & 0x01)
    GPIO.output(MUX_S3, (channel >> 3) & 0x01)

def read_mcp3008(channel=0):
    """
    Read the MCP3008 at the given channel (0..7).
    Returns a value 0..1023.
    """
    cmd1 = 1
    cmd2 = (8 + channel) << 4
    adc_response = spi.xfer2([cmd1, cmd2, 0])
    raw_adc = ((adc_response[1] & 3) << 8) | adc_response[2]
    return raw_adc

def close_sensors():
    """
    Clean up SPI resources, if desired.
    """
    spi.close()
