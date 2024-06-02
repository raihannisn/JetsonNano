# I2C_LCD_driver.py
# Source: https://gist.github.com/DenisFromHR/cc863375a6e19dce359d

import smbus2
import time

# for RPI version 1, use "bus = smbus.SMBus(0)"
# for RPI version 2, use "bus = smbus.SMBus(1)"
bus = smbus2.SMBus(1)

# LCD Address
ADDRESS = 0x27  # I2C address of the PCF8574T

# some constants for the LCD
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = 1       # Mode - Sending data
LCD_CMD = 0       # Mode - Sending command
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_BACKLIGHT = 0x08  # On
ENABLE = 0b00000100  # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

class lcd:
    def __init__(self):
        self.lcd_device = bus
        self.lcd_init()

    def lcd_init(self):
        self.lcd_byte(0x33, LCD_CMD)
        self.lcd_byte(0x32, LCD_CMD)
        self.lcd_byte(0x06, LCD_CMD)
        self.lcd_byte(0x0C, LCD_CMD)
        self.lcd_byte(0x28, LCD_CMD)
        self.lcd_byte(0x01, LCD_CMD)
        time.sleep(E_DELAY)

    def lcd_byte(self, bits, mode):
        bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
        bits_low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT

        self.lcd_device.write_byte(ADDRESS, bits_high)
        self.lcd_toggle_enable(bits_high)

        self.lcd_device.write_byte(ADDRESS, bits_low)
        self.lcd_toggle_enable(bits_low)

    def lcd_toggle_enable(self, bits):
        time.sleep(E_DELAY)
        self.lcd_device.write_byte(ADDRESS, (bits | ENABLE))
        time.sleep(E_PULSE)
        self.lcd_device.write_byte(ADDRESS, (bits & ~ENABLE))
        time.sleep(E_DELAY)

    def lcd_display_string(self, message, line):
        message = message.ljust(LCD_WIDTH, " ")
        self.lcd_byte(line, LCD_CMD)
        for i in range(LCD_WIDTH):
            self.lcd_byte(ord(message[i]), LCD_CHR)
