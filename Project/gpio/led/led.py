import RPi.GPIO as GPIO
from time import sleep

#led = '/sys/class/leds/led0/brightness'

GPIO.setmode(GPIO.BCM) 
GPIO.setup(led, GPIO.OUT)

try:
    while True: 
        echo '1 > /sys/class/leds/led0/brightness'
        print ("Led off")
        sleep(1)
        echo '0 > /sys/class/leds/led0/brightness'
        print ("Led off")
        sleep(1)
except:

