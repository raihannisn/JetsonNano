Automatic Waste Sorting System
This Python script is designed for an Automatic Waste Sorting System using a combination of computer vision and hardware control. It utilizes a Jetson Nano platform, GPIO pins for controlling stepper motors, a camera for object detection, and an LCD display for user feedback.

Installation

Hardware Requirements:

Jetson Nano or similar development board
28BYJ-48 stepper motor for trash can lid control
NEMA17 stepper motor for waste bin sorting
Raspberry Pi Camera module or USB webcam
I2C LCD display

Software Requirements:

Jetson.GPIO library for GPIO control
OpenCV for computer vision tasks
smbus2 for I2C communication with the LCD display
ONNX runtime for running deep learning models
Python 3.8

Installation Steps:

Install the required Python libraries using pip:

pip install Jetson.GPIO opencv-python-headless smbus2

Install ONNX runtime. Follow the installation instructions provided in the official documentation: ONNX Runtime GitHub
Hardware Setup:

Connect the 28BYJ-48 stepper motor to the specified GPIO pins (DIR_PIN, STEP_PIN, EN_PIN, IN1, IN2, IN3, IN4).
Connect the NEMA17 stepper motor to the specified DIR_PIN and STEP_PIN.
Connect the Raspberry Pi Camera module or USB webcam to the Jetson Nano.
Connect the I2C LCD display to the appropriate pins.
Usage
Running the Script:

Execute the Python script on the Jetson Nano:

python sampah_otomatis.py

Ensure that the script has necessary permissions to access GPIO and camera.
Operation:

The system continuously captures video frames from the camera and performs object detection using a pre-trained deep learning model (dataset1.onnx).
Detected objects are classified into categories (Plastic, Paper, Glass, Metal, Waste) based on the trained model.
Depending on the detected category, the NEMA17 stepper motor moves the waste bin to the appropriate position.
The 28BYJ-48 stepper motor controls the trash can lid, opening or closing it as needed.
User Interface:

The system provides feedback on the LCD display, indicating the current category being processed.
Object detection results are displayed in real-time on the connected monitor or display device.
Notes
Ensure proper wiring and connections for GPIO pins and hardware components.
Calibrate the system according to your specific hardware setup and requirements.
Fine-tune the object detection model or replace it with a custom-trained model for better performance on your target objects. 
![nvidia-jetson-nano-developer-kit-b01-442355](https://github.com/raihannisn/JetsonNano/assets/137723185/d40db8e1-61d5-4d8d-9b4e-03f7c90509a1)
