import time
import Jetson.GPIO as GPIO

servo_pin = 16  # Pin GPIO untuk servo

GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo_pin, GPIO.OUT)

pwm = GPIO.PWM(servo_pin, 50)  # Inisialisasi PWM dengan frekuensi 50 Hz
pwm.start(0)  # Mulai PWM dengan duty cycle 0

def set_angle(angle):
    duty = angle / 18 + 2
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)  # Tunggu 1 detik
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

try:
    while True:
        set_angle(90)  # Putar servo ke sudut 90 derajat
        time.sleep(1)  # Tunggu 1 detik
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
