import Jetson.GPIO as GPIO
import time

# Definisikan pin GPIO yang digunakan
IN1 = 17
IN2 = 18
IN3 = 27
IN4 = 22

# Setel pin GPIO ke mode BCM
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setel semua pin sebagai output
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# Langkah stepper motor
sequence = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]

# Fungsi untuk memutar stepper motor
def set_step(w1, w2, w3, w4):
    GPIO.output(IN1, w1)
    GPIO.output(IN2, w2)
    GPIO.output(IN3, w3)
    GPIO.output(IN4, w4)

# Fungsi untuk memutar motor sebesar derajat tertentu
def rotate(degree, steps_per_rev=4096):
    steps = int((steps_per_rev * degree) / 360)
    for _ in range(steps):
        for step in sequence:
            set_step(*step)
            time.sleep(0.002)  # Ubah delay jika perlu

try:
    # Putar motor sebesar 90 derajat
    rotate(90)
finally:
    # Bersihkan pengaturan GPIO
    GPIO.cleanup()
