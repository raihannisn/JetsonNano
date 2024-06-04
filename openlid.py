import Jetson.GPIO as GPIO
import time

# Definisikan pin GPIO yang digunakan
IN1 = 22
IN2 = 23
IN3 = 24
IN4 = 10

# Setel pin GPIO ke mode BCM
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setel semua pin sebagai output
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# Langkah stepper motor untuk maju dan mundur
sequence_forward = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]

sequence_backward = list(reversed(sequence_forward))

# Fungsi untuk memutar stepper motor
def set_step(w1, w2, w3, w4):
    GPIO.output(IN1, w1)
    GPIO.output(IN2, w2)
    GPIO.output(IN3, w3)
    GPIO.output(IN4, w4)

# Fungsi untuk memutar motor sebesar derajat tertentu
def rotate(degree, direction='forward', steps_per_rev=4096, delay=0.001):
    steps = int((steps_per_rev * degree) / 360)
    sequence = sequence_forward if direction == 'forward' else sequence_backward
    for _ in range(steps):
        for step in sequence:
            set_step(*step)
            time.sleep(delay)  # Ubah delay untuk mempercepat perputaran

try:
    # Putar motor sebesar 90 derajat ke arah maju
    rotate(45, direction='forward', delay=0.001)
    print("Motor telah mencapai 45 derajat.")
    
    # Kembali ke titik awal (0 derajat) dengan arah mundur
    rotate(45, direction='backward', delay=0.001)
    print("Motor telah kembali ke titik awal.")
finally:
    # Bersihkan pengaturan GPIO
    GPIO.cleanup()

# Berhenti setelah mencapai titik awal
print("Program dihentikan setelah motor kembali ke titik awal.")
