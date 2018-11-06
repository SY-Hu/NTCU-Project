from gpiozero import LineSensor
from signal import pause
import time

sensor = LineSensor(4)

while True:
    sensor.when_line = lambda: print('Line detected')
    sensor.when_no_line = lambda: print('No line detected')

