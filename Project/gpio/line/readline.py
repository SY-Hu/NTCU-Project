import RPi.GPIO as gpio
from signal import pause
import time

pin = 23

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(pin, gpio.IN)

while True:
    data = gpio.input(pin)
    print (data)
    time.sleep(0.05)
    

