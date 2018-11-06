import RPi.GPIO as gpio
from time import sleep

# Setup GPIO
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

# Setup LED
ledLeft = 25
ledRight = 12
gpio.setup(ledRight, gpio.OUT)
gpio.setup(ledLeft, gpio.OUT)

# Main Program
try:
    while True:
        gpio.output(ledLeft,gpio.HIGH)
        gpio.output(ledRight,gpio.LOW)
        sleep(1)
        gpio.output(ledLeft,gpio.LOW)
        gpio.output(ledRight,gpio.HIGH)
        sleep(1)
except:
    gpio.cleanup()