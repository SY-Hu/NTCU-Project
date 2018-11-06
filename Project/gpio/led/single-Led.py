import RPi.GPIO as GPIO
import time

pin = 19

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(pin, GPIO.OUT)

try:
    while True:	
        GPIO.output(pin,GPIO.HIGH)
        time.sleep(1)
        GPIO.output(pin,GPIO.LOW)
        time.sleep(1)
except:
    pass
finally:
    GPIO.cleanup()
