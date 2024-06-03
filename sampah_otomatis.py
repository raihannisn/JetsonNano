import Jetson.GPIO as GPIO
import time
import numpy as np
import cv2
import smbus2
import I2C_LCD_driver  # Pastikan Anda memiliki file I2C_LCD_driver.py di direktori yang sama

# Define pin assignments
DIR_PIN = 19  # Pin for direction (GPIO17, pin 11)
STEP_PIN = 20  # Pin for step (GPIO22, pin 15)
EN_PIN = 26   # Pin for enable (GPIO27, pin 13)
DELAY = 0.001  # Delay between steps in seconds

# Define the steps for each bin
steps_per_category = {
    "Plastic": 0,
    "Paper": 1300,
    "Glass": 1300,
    "Metal": 3900,
    "Waste": 3900
}

# Stepper motor pin assignments for bin lid
IN1 = 17
IN2 = 18
IN3 = 27
IN4 = 22

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup GPIO pins for sorting motor
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(STEP_PIN, GPIO.OUT)
GPIO.setup(EN_PIN, GPIO.OUT)

# Setup GPIO pins for bin lid motor
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# Langkah stepper motor untuk tutup tong sampah
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

# Function to initialize motor
def initialize_motor():
    GPIO.output(DIR_PIN, GPIO.LOW)  # Set direction (HIGH for one direction, LOW for the other)
    GPIO.output(EN_PIN, GPIO.LOW)   # Enable motor (LOW to enable, HIGH to disable)

# Function to step the motor
def step_motor(steps, delay=DELAY):
    print("Motor starting...")
    for step in range(steps):
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(delay)
    print("Motor stopped.")

# Function to sort trash based on label
def sort_trash(label):
    if label in steps_per_category:
        steps = steps_per_category[label]
        step_motor(steps)
        print(f"Motor berjalan {steps} langkah untuk {label}")

# Function to set step for stepper motor (bin lid)
def set_step(w1, w2, w3, w4):
    GPIO.output(IN1, w1)
    GPIO.output(IN2, w2)
    GPIO.output(IN3, w3)
    GPIO.output(IN4, w4)

# Function to rotate bin lid motor
def rotate_lid(degree, steps_per_rev=4096):
    steps = int((steps_per_rev * degree) / 360)
    for _ in range(steps):
        for step in sequence:
            set_step(*step)
            time.sleep(0.002)  # Ubah delay jika perlu

# Inisialisasi LCD
lcd = I2C_LCD_driver.lcd()

# Object detection and classification setup
classes = ["Plastic", "Paper", "Glass", "Metal", "Waste"]
cap = cv2.VideoCapture(0)
net = cv2.dnn.readNetFromONNX("dataset1.onnx")

try:
    initialize_motor()
    while True:
        _, img = cap.read()

        blob = cv2.dnn.blobFromImage(img, scalefactor=1/255, size=[640, 640], mean=[0, 0, 0], swapRB=True, crop=False)
        net.setInput(blob)
        detections = net.forward()[0]

        classes_ids = []
        confidences = []
        boxes = []
        rows = detections.shape[0]

        img_width, img_height = img.shape[1], img.shape[0]
        x_scale = img_width / 640
        y_scale = img_height / 640

        for i in range(rows):
            row = detections[i]
            confidence = row[4]
            if confidence > 0.2:
                classes_score = row[5:]
                ind = np.argmax(classes_score)
                if classes_score[ind] > 0.2:
                    classes_ids.append(ind)
                    confidences.append(confidence)
                    cx, cy, w, h = row[:4]
                    x1 = int((cx - w / 2) * x_scale)
                    y1 = int((cy - h / 2) * y_scale)
                    width = int(w * x_scale)
                    height = int(h * y_scale)
                    box = np.array([x1, y1, width, height])
                    boxes.append(box)

        indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.2)

        for i in indices:
            x1, y1, w, h = boxes[i]
            label = classes[classes_ids[i]]
            conf = confidences[i]
            text = label + "{:.2f}".format(conf)
            cv2.rectangle(img, (x1, y1), (x1 + w, y1 + h), (255, 0, 0), 2)
            cv2.putText(img, text, (x1, y1 - 2), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)

            # Tampilkan label di LCD
            lcd.lcd_display_string(f"Label: {label}", 1)

        # Panggil fungsi sort_trash setelah semua objek dideteksi
        for i in indices:
            label = classes[classes_ids[i]]
            sort_trash(label)
            
            # Buka tutup tong sampah
            lcd.lcd_display_string("Tutup Terbuka", 2)
            rotate_lid(90)
            time.sleep(5)  # Tahan tutup tetap terbuka selama 5 detik
            lcd.lcd_display_string("Tutup Tertutup", 2)
            rotate_lid(-90)  # Tutup kembali

        cv2.imshow("Deteksi Objek", img)
        if cv2.waitKey(1) & 0xff == 27:
            break

finally:
    GPIO.cleanup()
    cap.release()
    cv2.destroyAllWindows()
    print("GPIO cleanup done.")
