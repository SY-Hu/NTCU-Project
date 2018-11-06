import RPi.GPIO as GPIO
from subprocess import call
from time import sleep

try:
    while True:
        call(["echo","1>/sys/class/leds/led0/brightness"])
        print("Led on")
        sleep(1)
        call(["echo","0>/sys/class/leds/led0/brightness"])
        print("Led off")
        sleep(1)
except:
    print("Exit")
