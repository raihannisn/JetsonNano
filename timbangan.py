import Jetson.GPIO as GPIO
from hx711 import HX711
import time

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)

# Pin definitions
DT_PIN = 17  # Data Pin
SCK_PIN = 27  # Clock Pin

# Initialize HX711
hx = HX711(dout_pin=DT_PIN, pd_sck_pin=SCK_PIN)

# Function to clean up GPIO pins
def cleanAndExit():
    print("Cleaning...")
    GPIO.cleanup()
    print("Bye!")
    sys.exit()

# Set the reference unit (calibration factor)
hx.set_reference_unit(92)

hx.reset()
hx.tare()

print("Tare done! Add weight now...")

try:
    while True:
        # Read the current weight
        val = hx.get_weight(5)
        # Convert the reading to kilograms
        weight_in_kg = val / 1000.0
        print("Weight: {} kg".format(weight_in_kg))
        
        hx.power_down()
        hx.power_up()
        time.sleep(0.1)

except (KeyboardInterrupt, SystemExit):
    cleanAndExit()
