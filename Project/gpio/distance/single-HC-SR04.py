import RPi.GPIO as gpio
import sys
import time
from time import sleep

########## Global Variable ##########
maxDistance = 20
freq        =  1
echo        = 16
trig        = 17
led         = 18
ir          = None

########## Basic Setup ##########
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
if not led == None:
    gpio.setup(led, gpio.OUT)
if not ir == None:
    gpio.setup(ir, gpio.IN)

gpio.setup(trig, gpio.OUT)
gpio.setup(echo, gpio.IN)

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
        if not led == None:
            gpio.output(led,gpio.LOW)
        
        distance = distanceCalc(echo,trig)
        print("[Distance] Distance: %10f" % (distance)) 
         
        if not led == None and distance < maxDistance:
            gpio.output(led,gpio.HIGH)
        
        sleep(1/freq)

except BaseException as e:
    print("[Distance] Get Exception.")
    print(type(e),str(e))

finally:
    gpio.cleanup()
