import Jetson.GPIO as GPIO
import time

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

STEP_PIN = 17
DIR_PIN = 18
EN_PIN = 19

GPIO.setup(STEP_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(EN_PIN, GPIO.OUT)

# Enable the motor
GPIO.output(EN_PIN, GPIO.LOW)

# Set direction (0 or 1)
GPIO.output(DIR_PIN, GPIO.HIGH)  # or GPIO.LOW

# Function to move stepper motor
def move_stepper(steps, delay):
    for i in range(steps):
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(delay)
        print(f"Step {i + 1}/{steps}")

# Main
steps = 1000
delay = 0.001  # Start with a larger delay for testing, adjust as needed

try:
    move_stepper(steps, delay)
finally:
    # Cleanup
    GPIO.output(EN_PIN, GPIO.HIGH)  # Disable the motor
    GPIO.cleanup()

print("Stepper motor movement complete.")
