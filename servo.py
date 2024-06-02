import Jetson.GPIO as GPIO
import time

# Tentukan nomor pin GPIO yang mendukung PWM
servo_pin = 33  # Nomor GPIO untuk pin 33

# Setup GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo_pin, GPIO.OUT)

# Setup PWM
pwm = GPIO.PWM(servo_pin, 50)  # Frekuensi PWM 50Hz
pwm.start(0)

def set_angle(angle):
    GPIO.setup(servo_pin, GPIO.OUT)  # Pastikan pin diatur sebagai output
    duty = angle / 18 + 2
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

try:
    while True:
        # Buka servo ke 90 derajat
        set_angle(90)
        time.sleep(1)
        
        # Tutup servo ke titik awal (0 derajat)
        set_angle(0)
        time.sleep(1)

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
