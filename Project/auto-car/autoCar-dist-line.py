#! /usr/bin/python
import RPi.GPIO as gpio
import sys
import time
from time import sleep

# Set up DistanceSensor
from gpiozero import DistanceSensor
echo = 6
trigger = 12
distanceSensor = DistanceSensor(echo, trigger)

# Set up LineSensor
#from gpiozero import LineSensor
#lineSensor = LineSensor(4)
#lineSensor.when_line = lambda : getLine(True)
#lineSensor.when_no_line = lambda : getLine(False)
#onLine = False

#def getLine(data):
#    global onLine
#    onLine = data

readlineL = 7
readlineR = 19

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)

gpio.setup(readlineL,gpio.IN)
gpio.setup(readlineR,gpio.IN)


# Define function to command the car
def go():
    motor = [60,0,60,0]

def stop():
    motor = [0,0,0,0]

def back():
    motor = [0,60,0,60]

def turnRight():
    motor = [50,0,0,50]

def right():
    motor[0]+= 3
    motor[2]-= 3

def turnLeft():
    motor = [0,50,50,0]

def left():
    motor[0]-= 3
    motor[2]+= 3

def slowGo():
    motor = [45,0,45,0]

# Define input pin
ain1 = 11 
ain2 = 12
ain3 = 13
ain4 = 16

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

while True:
    if gpio.input(readlineL) == 1 and gpio.input(readlineR) == 1 and distanceSensor.distance > 12:
        go()
    elif onLine == False and distanceSensor.distance > 12:
        shiftL = 0
        shiftR = 0
        i = 0
        slowGo()
        while i < 10:
            if distanceSensor.distance < 12:
                stop()
                break
            elif onLine == True:
                break
#CONTINUE

            elif onLine == False:
                # seek left
                if shiftL >= shiftR :
                    for x in range (i):
                        left()
                        shiftL += 1
                      
    elif distanceSensor.distance < 12:
        stop()
        sleep(1)
        turnRight()
        sleep(1.5)







   # protect motor
    for i in range(4):
        if motor[i] > 100:
            motor[i] = 100
            print("motor [",i,"] is too large")
        elif motor[i] < 0:
            motor[i] = 0
            print("motor [",i,"] is too small")


    print(motor[0],motor[1],motor[2],motor[3], ss, ts)
    #set to motor
    m1.ChangeDutyCycle(motor[0])
    m2.ChangeDutyCycle(motor[1])
    m3.ChangeDutyCycle(motor[2])
    m4.ChangeDutyCycle(motor[3])

gpio.cleanup()
