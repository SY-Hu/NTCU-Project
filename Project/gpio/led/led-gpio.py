import RPi.GPIO as GPIO
from time import sleep

led = 16

GPIO.setmode(GPIO.BOARD) 
GPIO.setup(16, GPIO.OUT)

try:
    while True:
        GPIO.output(16,GPIO.LOW)
        print "Led on"
        sleep(1)
        GPIO.output(16,GPIO.HIGH)
        print "Led off"
        sleep(1)
except:
    GPIO.cleanup()
