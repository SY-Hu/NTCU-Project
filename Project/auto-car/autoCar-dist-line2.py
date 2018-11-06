#! /usr/bin/python
import RPi.GPIO as gpio
import sys
import time
from time import sleep
# Setup Global Variable
maxDistance = 20
enableTraceLine = False

# Setup GPIO
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)

# Setup LED
ledLeft = 23
ledRight = 24
gpio.setup(ledRight, gpio.OUT)
gpio.setup(ledLeft, gpio.OUT)

# Setup DistanceSensor
echo1 = 38
echo2 = 36
trigger1 = 37
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
    if TimeElapsed <= 0:
        TimeElapsed = 1
        print(pin ,' time too small.')
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    
    if distance > 500:
        distance = 500

    return distance

# Set up LineSensor

readlineL = 29
readlineM = 31
readlineR = 32

gpio.setup(readlineL,gpio.IN)
gpio.setup(readlineM,gpio.IN)
gpio.setup(readlineR,gpio.IN)


# Define function to command the car
def go():
    motor[0:3] = [55,0,40,0]
    gpio.output(ledLeft,gpio.LOW)
    gpio.output(ledRight,gpio.LOW)
    exe()

def stop():
    motor[0:3] = [0,0,0,0]
    gpio.output(ledLeft,gpio.HIGH)
    gpio.output(ledRight,gpio.HIGH)
    exe()

def back():
    motor[0:3] = [0,50,0,50]
    gpio.output(ledLeft,gpio.LOW)
    gpio.output(ledRight,gpio.LOW)
    exe()

def turnRight():
    motor[0:3] = [50,0,0,50]
    gpio.output(ledLeft,gpio.LOW)
    gpio.output(ledRight,gpio.HIGH)
    exe()

def right():
    #motor[0]+= 3
    #motor[2]-= 3
    motor[0:3] = [45,0,75,0]
    gpio.output(ledLeft,gpio.LOW)
    gpio.output(ledRight,gpio.HIGH)
    exe()

def turnLeft():
    motor[0:3] = [0,50,50,0]
    gpio.output(ledLeft,gpio.HIGH)
    gpio.output(ledRight,gpio.LOW)
    exe()

def left():
    #motor[0]-= 3
    #motor[2]+= 3
    motor[0:3] = [70,0,55,0]
    gpio.output(ledLeft,gpio.HIGH)
    gpio.output(ledRight,gpio.LOW)
    exe()

def slowGo():
    motor[0:3] = [40,0,40,0]
    gpio.output(ledLeft,gpio.LOW)
    gpio.output(ledRight,gpio.LOW)
    exe()

def exe():
    
    for i in range(4):
        if motor[i] > 100:
            motor[i] = 100
            print("motor [",i,"] is too large")
        elif motor[i] < 0:
            motor[i] = 0
            print("motor [",i,"] is too small")


    print("motor:{0:d},{1:d},{2:d},{3:d}".format(motor[0],motor[1],motor[2],motor[3]))
    #set to motor
    m1.ChangeDutyCycle(motor[0])
    m2.ChangeDutyCycle(motor[1])
    m3.ChangeDutyCycle(motor[2])
    m4.ChangeDutyCycle(motor[3])



# Define input pin
ain1 = 10 
ain2 = 11
ain3 = 12
ain4 = 13
#ain1 = 17
#ain2 = 18
#ain3 = 27
#ain4 = 23


# Set default duty cycle
motor = [0,0,0,0] # L1,L2 , R1,R2
 
#gpio.setwarnings(False)
#gpio.setmode(gpio.BOARD)
gpio.setup(ain1, gpio.OUT)
gpio.setup(ain2, gpio.OUT)
gpio.setup(ain3, gpio.OUT)
gpio.setup(ain4, gpio.OUT)

# Set to gpio 
m1 = gpio.PWM(ain1, 30)
m2 = gpio.PWM(ain2, 30)
m3 = gpio.PWM(ain3, 30)
m4 = gpio.PWM(ain4, 30)

m1.start(0)
m2.start(0)
m3.start(0)
m4.start(0)

print("Setup Finished")

try:
    while True:
        readL = gpio.input(readlineL)
        readR = gpio.input(readlineR)
        distanceR = distanceCalc(echo1, trigger1)
        distanceL = distanceCalc(echo2, trigger2)
  
        #UI
        print('DisL  LineL  LineR  DisR  ')
        print('{0:3.2f}  {1:d}      {2:d}    {3:3.2f}'.format(distanceL,readL,readR,distanceR))





        if readL == 0 and readR == 0 and distanceL > maxDistance and distanceR > maxDistance:
            print("Command: GO        ", end='')
            go()
        elif readL == 1 and readR == 0 and distanceL > maxDistance and distanceR > maxDistance and enableTraceLine:
            # Go Left
            print("Command: LEFT      ", end='')
            left()
            sleep(0.3)
        elif readL == 0 and readR == 1 and distanceL > maxDistance and distanceR > maxDistance and enableTraceLine:
            # Go Right
            print("Command: RIGHT     ", end='')
            right()
            sleep(0.3)
        elif distanceL < maxDistance or distanceR < maxDistance:
            print("Command: STOP      ", end='')
            stop()
            if distanceL < 8 or distanceR < 8:
                print("Command: BACK      ", end='')
                back()
                sleep(0.2)
                print("Command: STOP      ", end='')
                stop()
            sleep(0.8)
            if distanceL < maxDistance:
                print("Command: RUEN RIGHT", end='')
                turnRight()
            elif distanceR < maxDistance:
            #    print("Command: TURN LEFT ", end='')
            #    turnLeft()
                print("Command: TURN RIGHT ", end='')
                turnRight()
            else:
                print("Command: RUEN RIGHT", end='')
                turnRight()
            sleep(0.2)
        else:
            print("Command: Slow Go   ", end='')
            slowGo()
        
        # UI status
        if readL == 1 and readR == 1:
            print("Car can't find line.")
        else:
            print(" ")


        print('==========================')

        sleep(0.05)
except:    
    print("Command: FORCE STOP ", end='')
    stop()
    gpio.cleanup()
