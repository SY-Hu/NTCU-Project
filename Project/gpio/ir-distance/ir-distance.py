import RPi.GPIO as gpio
import time

# Setup Variable
pin = 13

# Setup GPIO
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

# Setup IR-DistanceSensor
gpio.setup(pin,gpio.IN)

while True:
    print(gpio.input(pin))
    time.sleep(0.01)
    
