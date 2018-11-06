import RPi.GPIO as gpio
import sys
import time
from time import sleep
# Setup Global Variable
maxDistance = 20

# Setup GPIO
gpio.setwarnings(True)
gpio.setmode(gpio.BOARD)


# Setup LED
ledDisLeft = 21
ledDisRight = 22
gpio.setup(ledDisRight, gpio.OUT)
gpio.setup(ledDisLeft, gpio.OUT)


# Setup DistanceSensor
echo1 = 38
#echo1 = 15
echo2 = 36
trigger1 = 37
#trigger1 = 16
trigger2 = 35
gpio.setup(trigger1, gpio.OUT)
gpio.setup(trigger2, gpio.OUT)
gpio.setup(echo1, gpio.IN)
gpio.setup(echo2, gpio.IN)

def distanceCalc(pin,tri):
    # set Trigger to HIGH
    gpio.output(tri, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
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
    gpio.output(ledDisLeft,gpio.LOW)
    gpio.output(ledDisRight,gpio.LOW)
    while True:
        gpio.output(ledDisLeft,gpio.LOW)
        distanceL = distanceCalc(echo2, trigger2)
        print('DistanceL: ', distanceL)
        if distanceL < maxDistance:
            gpio.output(ledDisLeft,gpio.HIGH)

        sleep(0.05)

        gpio.output(ledDisRight,gpio.LOW)
        distanceR = distanceCalc(echo1, trigger1)
        print('DistanceR: ', distanceR)
        if distanceR < maxDistance:
            gpio.output(ledDisRight,gpio.HIGH)
        
        sleep(0.05)
except:
    print('EXCEPT')
    gpio.cleanup()
