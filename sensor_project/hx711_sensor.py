import RPi.GPIO as GPIO
import time

class HX711:
    def __init__(self, dout_pin, pd_sck_pin, gain=128):
        self.PD_SCK = pd_sck_pin
        self.DOUT = dout_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)  # Disable warnings about pins already in use
        GPIO.setup(self.PD_SCK, GPIO.OUT)
        GPIO.setup(self.DOUT, GPIO.IN)

        self.GAIN = 0
        self.set_gain(gain)

    def set_gain(self, gain):
        if gain == 128:
            self.GAIN = 1
        elif gain == 64:
            self.GAIN = 3
        elif gain == 32:
            self.GAIN = 2
        else:
            raise ValueError("Invalid gain value. Use 128, 64, or 32.")
        self.read()  # Read to set the gain

    def read(self):
        # Wait for the chip to become ready
        while GPIO.input(self.DOUT) == 1:
            pass

        count = 0
        for _ in range(24):
            GPIO.output(self.PD_SCK, True)
            count = count << 1
            GPIO.output(self.PD_SCK, False)
            if GPIO.input(self.DOUT):
                count += 1

        # Set the gain for the next reading
        for _ in range(self.GAIN):
            GPIO.output(self.PD_SCK, True)
            GPIO.output(self.PD_SCK, False)

        # Convert the result to signed integer
        if count & 0x800000:
            count -= 0x1000000

        return count

    def clean_and_exit(self):
        GPIO.cleanup()

