import RPi.GPIO as gpio
import sys
import time
from time import sleep
# Setup Global Variable
maxDistance = 20
left = False
right = True
distanceL = 0
distanceR = 0
freq = 1

# Setup GPIO
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)


# Setup LED
ledDisLeft = 24
ledDisRight = 7
gpio.setup(ledDisRight, gpio.OUT)
gpio.setup(ledDisLeft, gpio.OUT)


# Setup DistanceSensor
echo1 = 19
echo2 = 16
trigger1 = 20
trigger2 = 17
gpio.setup(trigger1, gpio.OUT)
gpio.setup(trigger2, gpio.OUT)
gpio.setup(echo1, gpio.IN)
gpio.setup(echo2, gpio.IN)

def distanceCalc(pin,tri):
    # set Trigger to HIGH
    gpio.output(tri, True)

    # set Trigger after 0.1ms to LOW
    time.sleep(0.0001)
    gpio.output(tri, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while gpio.input(pin) == 0:
        StartTime = time.time()

    # save time of arrival
    while gpio.input(pin) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    if TimeElapsed <= 0 :
        TimeElapsed = 1
        print('Time too small')
    
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    if distance > 500:
        distance = 500

    return distance

try:
    while True:
        if left:
            gpio.output(ledDisLeft,gpio.LOW)
            distanceL = distanceCalc(echo2, trigger2)
        if right:
            gpio.output(ledDisRight,gpio.LOW)
            distanceR = distanceCalc(echo1, trigger1)

        print("DistanceL: %10f    DistanceR: %10f" % (distanceL,distanceR)) 
         
        # Led Control
        if distanceL < maxDistance:
            gpio.output(ledDisLeft,gpio.HIGH)
        if distanceR < maxDistance:
            gpio.output(ledDisRight,gpio.HIGH)
        
        sleep(1/freq)
except:
    print('EXCEPT')
    gpio.cleanup()
