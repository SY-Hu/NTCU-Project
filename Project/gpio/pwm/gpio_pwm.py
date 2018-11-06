import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)

ain1 = 11
ain2 = 12

GPIO.setup(ain1, GPIO.OUT)
GPIO.setup(ain2, GPIO.OUT)


p1 = GPIO.PWM(ain1, 50)
p2 = GPIO.PWM(ain2, 50)
p1.start(0)
p2.start(0)
try:
    while 1:
        for dc in range(0, 101, 5):
            p1.ChangeDutyCycle(dc)
            p2.ChangeDutyCycle(dc)
            print(dc)
            time.sleep(0.1)
        for dc in range(100, -1, -5):
            p1.ChangeDutyCycle(dc)
            p2.ChangeDutyCycle(dc)
            print(dc)
            time.sleep(0.1)
except KeyboardInterrupt:
    pass
p1.stop()
p2.stop()
GPIO.cleanup()
