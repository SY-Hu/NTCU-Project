import RPi.GPIO as gpio
from time import sleep

# Setup GPIO
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

# Setup LED
ledDisLeft = 24
ledDisRight = 7
gpio.setup(ledDisRight, gpio.OUT)
gpio.setup(ledDisLeft, gpio.OUT)

# Main Program
try:
    while True:
        gpio.output(ledDisLeft,gpio.HIGH)
        gpio.output(ledDisRight,gpio.LOW)
        sleep(1)
        gpio.output(ledDisLeft,gpio.LOW)
        gpio.output(ledDisRight,gpio.HIGH)
        sleep(1)
except:
    gpio.cleanup()