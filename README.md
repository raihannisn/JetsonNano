# Automatic Waste Sorting System

![Waste Sorting System](waste_sorting_system.jpg)

## Overview

This Python script implements an Automatic Waste Sorting System using computer vision and hardware control. It is designed to run on a Jetson Nano platform and utilizes GPIO pins for controlling stepper motors, a camera for object detection, and an LCD display for user feedback.

## Features

- Real-time object detection and classification
- Automatic sorting of waste into categories (Plastic, Paper, Glass, Metal, Waste)
- Control of NEMA17 stepper motor for waste bin sorting
- Control of 28BYJ-48 stepper motor for trash can lid opening/closing
- User feedback via LCD display
- Supports Python 3.8
- Compatible with Ubuntu 20.04

## Installation

### Hardware Requirements:

- Jetson Nano or similar development board
- 28BYJ-48 stepper motor
- NEMA17 stepper motor
- Raspberry Pi Camera module or USB webcam
- I2C LCD display

### Software Requirements:

- Python 3.8
- Jetson.GPIO
- OpenCV
- smbus2
- ONNX runtime

### Installation Steps:

1. Install Python 3.8:
   ```bash
   sudo apt update
   sudo apt install python3.8 python3.8-dev
