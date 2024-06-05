import Jetson.GPIO as GPIO
import time

# Stepper motor configurations for 28BYJ-48
IN1 = 22
IN2 = 23
IN3 = 24
IN4 = 10

GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# Stepper motor sequence for 28BYJ-48
SEQ = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]

def move_stepper_motor(steps, direction):
    steps = abs(steps)
    for _ in range(steps):
        for step in range(8):
            for pin in range(4):
                GPIO.output([IN1, IN2, IN3, IN4][pin], SEQ[step][pin] if direction == GPIO.HIGH else SEQ[7 - step][pin])
            time.sleep(0.001)

def open_lid():
    move_stepper_motor(512, GPIO.HIGH)  # Adjust steps according to the motor specifications
    time.sleep(5)  # Delay to keep the lid open for 5 seconds

def close_lid():
    move_stepper_motor(512, GPIO.LOW)  # Adjust steps according to the motor specifications
