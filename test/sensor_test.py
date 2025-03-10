import time
import spidev
import RPi.GPIO as GPIO

# -----------------------------
# 1) SETUP GPIO / SPI
# -----------------------------
# MUX select pins
MUX_S0 = 17
MUX_S1 = 27
MUX_S2 = 22
MUX_S3 = 23

GPIO.setmode(GPIO.BCM) # GPIO pin number
for pin in [MUX_S0, MUX_S1, MUX_S2, MUX_S3]: # Initialize GPIO
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

# The Pi uses SPI (via MOSI, MISO, SCLK, and CE lines) to send commands to the MCP3008 and read back the converted analog values.
spi = spidev.SpiDev()       # Initialize SPI for MCP3008 
spi.open(0, 0)              # talk over the primary SPI pins (bus 0) and automatically pull CE0 low when we need to communicate with the ADC
spi.max_speed_hz = 1350000  # a typical safe speed

# -----------------------------
# 2) FUNCTIONS
# -----------------------------

def set_mux_channel(channel):
    """
    Given a channel number (0..15),
    set the 4 select pins (S0..S3) to route
    that channel's signal to SIG on the MUX.
    """
    # e.g. if channel is 3 (binary 0011), it sets S0 and S1 to HIGH (1) and S2 and S3 to LOW (0), which tells the MUX: “Link C3 to the SIG pin.”
    GPIO.output(MUX_S0, channel & 0x01)
    GPIO.output(MUX_S1, (channel >> 1) & 0x01)
    GPIO.output(MUX_S2, (channel >> 2) & 0x01)
    GPIO.output(MUX_S3, (channel >> 3) & 0x01)

def read_mcp3008(adc_channel=0):
    """
    Reads from MCP3008 channel 0..7.
    Returns a raw value from 0..1023 (10-bit ADC).
    """
    cmd1 = 1                                    # set 1 to let MCP3008 know that data is ready to be sent
    cmd2 = 8 + adc_channel << 4                 # set which channel to sent: 8 + 0 = 8 (binary 1000), shifting 4 bit: 1000 0000
    adc_response = spi.xfer2([cmd1, cmd2, 0])   # set 0000 0000 for extra clock pulses to receive the rest 8 bits of data

    # 10 bits of ADC data end up in adc_response[1] and adc_response[2], each 8 bits, where it's in the last two bits of adc_response[1] and all 8 bits of adc_response[2]
    raw_adc = ((adc_response[1] & 3) << 8) | adc_response[2]
    return raw_adc

# -----------------------------
# 3) MAIN LOOP: READ SENSORS
# -----------------------------

try:
    while True:
        # for mux_channel in [0, 1, 2, 3]:            # Example: Suppose we have sensors on MUX channels 0..3
        for mux_channel in [0]:
            set_mux_channel(mux_channel)            # 1) Select the channel on the MUX
            raw_value = read_mcp3008(adc_channel=0) # 2) Read from MCP3008 channel 0 (the MUX is wired to CH0)
            voltage = (raw_value * 3.3) / 1023.0    # 3) Convert raw_value (0..1023) to voltage (0..3.3)
            print(f"MUX channel {mux_channel}: raw={raw_value} voltage={voltage:.3f} V")

        print("---")
        time.sleep(1.0)  # read every 1 second

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
    spi.close()
