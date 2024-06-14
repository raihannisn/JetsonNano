import Jetson.GPIO as GPIO
import time
import numpy as np
import cv2
import smbus2
import I2C_LCD_driver

# Pin configurations
DIR_PIN = 19
STEP_PIN = 20
EN_PIN = 26
DELAY = 0.001

# Stepper motor configurations for 28BYJ-48
IN1 = 22
IN2 = 23
IN3 = 24
IN4 = 10

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(STEP_PIN, GPIO.OUT)
GPIO.setup(EN_PIN, GPIO.OUT)
GPIO.output(EN_PIN, GPIO.LOW)

# Stepper motor pins setup
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

# Function to move 28BYJ-48 stepper motor
def move_stepper_motor(steps, direction):
    steps = abs(steps)
    for _ in range(steps):
        for step in range(8):
            for pin in range(4):
                GPIO.output([IN1, IN2, IN3, IN4][pin], SEQ[step][pin] if direction == GPIO.HIGH else SEQ[7 - step][pin])
            time.sleep(0.001)

# Function to move NEMA17 stepper motor
def move_motor(steps, direction):
    GPIO.output(DIR_PIN, direction)
    GPIO.output(EN_PIN, GPIO.HIGH)  # Enable motor
    for _ in range(abs(steps)):
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(DELAY)
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(DELAY)
    GPIO.output(EN_PIN, GPIO.LOW)  # Disable motor

# Example function to open and close trash can lid
def control_trash_can_lid():
    # Open the trash can lid
    move_stepper_motor(97, GPIO.HIGH)
    print("Lid opened")
    time.sleep(5)
    
    # Close the trash can lid
    move_stepper_motor(97, GPIO.LOW)
    print("Lid closed")

# Initialize LCD
lcd = I2C_LCD_driver.lcd()

classes = ["Plastic", "Paper", "Glass", "Metal", "Waste"]
steps_per_category = {
    "Plastic": 0,
    "Paper": 1300,
    "Glass": 1300,
    "Metal": 3900,
    "Waste": 3900
}

cap = cv2.VideoCapture(0)
net = cv2.dnn.readNetFromONNX("dataset1.onnx")

motor_returned = False
current_label = None

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

    detected_label = None
    for i in indices:
        x1, y1, w, h = boxes[i]
        detected_label = classes[classes_ids[i]]
        cv2.rectangle(img, (x1, y1), (x1 + w, y1 + h), (255, 0, 0), 2)
        cv2.putText(img, detected_label, (x1, y1 - 2), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)
        break

    if detected_label and detected_label != current_label:
        current_label = detected_label
        
        steps = steps_per_category[current_label]
        move_motor(steps, GPIO.LOW if steps >= 0 else GPIO.HIGH)
        
        # Open and close the trash can lid
        control_trash_can_lid()
        
        move_motor(-steps, GPIO.HIGH if steps >= 0 else GPIO.LOW)
        
        # Update the LCD display after processing is done
        lcd.lcd_display_string(f"Kategori: {current_label}", 1)
        motor_returned = True

    cv2.imshow("Deteksi Objek", img)
    if cv2.waitKey(1) & 0xff == 27 or motor_returned:
        break

cap.release()
cv2.destroyAllWindows()
GPIO.cleanup()
