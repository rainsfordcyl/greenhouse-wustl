import spidev
import RPi.GPIO as GPIO

spi = spidev.SpiDev()

def init_sensors():
    """
    Sets up SPI for the MCP3008.
    Call this once at program startup.
    """
    # If you're not using the MUX, you don't need to configure MUX pins here
    # Just open the SPI interface
    spi.open(0, 0)
    spi.max_speed_hz = 1350000

def read_mcp3008(channel=0):
    """
    Reads the MCP3008 at the given channel (0..7).
    Returns an integer 0..1023.
    e.g. read_mcp3008(0) -> sensor on CH0, read_mcp3008(1) -> sensor on CH1, etc.
    """
    cmd1 = 1
    cmd2 = (8 + channel) << 4
    adc_response = spi.xfer2([cmd1, cmd2, 0])

    # Reconstruct the 10-bit reading from the last two bytes
    raw_adc = ((adc_response[1] & 3) << 8) | adc_response[2]
    return raw_adc

def close_sensors():
    """
    Close the SPI connection if desired.
    """
    spi.close()