import RPi.GPIO as GPIO
from subprocess import call
from time import sleep

try:
    while True:
        call(["sudo","./openLED.sh"])
        print("Led on")
        sleep(1)
        call(["sudo","./closeLED.sh"])
        print("Led off")
        sleep(1)
except:
    print("Exit")
