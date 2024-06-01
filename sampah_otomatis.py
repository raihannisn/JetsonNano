import numpy as np
import cv2
import Jetson.GPIO as GPIO
import time
from adafruit_servokit import ServoKit

classes = ["Plastic", "Paper", "Glass", "Metal", "Waste"]
cap = cv2.VideoCapture(0)
net = cv2.dnn.readNetFromONNX("dataset1.onnx")

# GPIO pin setup
DIR = 21
EN = 22
STEP = 30

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(EN, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(STEP, GPIO.OUT, initial=GPIO.LOW)

# Servo setup
kit = ServoKit(channels=16)
servo_channel = 0  # Sesuaikan dengan channel servo yang digunakan
open_angle = 90  # Sudut terbuka
close_angle = 0  # Sudut tertutup
kit.servo[servo_channel].angle = close_angle

# Define the steps for each bin
steps_per_category = {
    "Plastic": 0,
    "Glass": 500,
    "Paper": 1000,
    "Waste": 1000,
    "Metal": 1500
}

def run_motor(target_steps, delay=0.005):
    GPIO.output(EN, GPIO.LOW)  # Enable the motor driver
    GPIO.output(DIR, GPIO.HIGH)  # Set direction
    for _ in range(target_steps):
        GPIO.output(STEP, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        time.sleep(delay)
    GPIO.output(EN, GPIO.HIGH)  # Disable the motor driver

def return_motor_to_zero(target_steps, delay=0.005):
    GPIO.output(EN, GPIO.LOW)  # Enable the motor driver
    GPIO.output(DIR, GPIO.LOW)  # Set direction to reverse
    for _ in range(target_steps):
        GPIO.output(STEP, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        time.sleep(delay)
    GPIO.output(EN, GPIO.HIGH)  # Disable the motor driver

def sort_trash(label):
    if label in steps_per_category:
        target_steps = steps_per_category[label]
        run_motor(target_steps)
        print(f"Motor berjalan {target_steps} langkah untuk {label}")
        
        # Buka tutup tong sampah
        print("Membuka tutup tong sampah")
        kit.servo[servo_channel].angle = open_angle
        time.sleep(2)  # Tunggu beberapa detik agar sampah bisa masuk

        # Tutup kembali tutup tong sampah
        print("Menutup tutup tong sampah")
        kit.servo[servo_channel].angle = close_angle
        
        # Kembalikan motor ke titik 0
        print("Mengembalikan ke titik 0")
        return_motor_to_zero(target_steps)
        print("Menunggu 60 detik")
        time.sleep(60)

try:
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
        x_scale = img_width/640
        y_scale = img_height/640

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
                    x1 = int((cx-w/2)*x_scale)
                    y1 = int((cy-h/2)*y_scale)
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
            cv2.rectangle(img, (x1, y1), (x1+w, y1+h), (255, 0, 0), 2)
            cv2.putText(img, text, (x1, y1-2), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)

            sort_trash(label)

        cv2.imshow("Deteksi Objek", img)
        if cv2.waitKey(1) & 0xff == 27:
            break

finally:
    GPIO.cleanup()
    cap.release()
    cv2.destroyAllWindows()
