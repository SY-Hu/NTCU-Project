import RPi.GPIO as gpio
from signal import pause
import time

pin = 19

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(pin, gpio.IN)

while True:
    data = gpio.input(pin)
    print (data)
    time.sleep(0.2)
    

