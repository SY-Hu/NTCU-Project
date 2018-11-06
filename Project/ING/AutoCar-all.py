#! /usr/bin/python

#########################################
# NTCU Computer Science 
# Project 107 - 08 
# Program : Auto TraceLine Car
#            with Wifi Sender
#########################################

print("NTCU Computer Science Project 107-08")
print("Program : Auto TraceLine Car with Wifi Sender")
print("Program AutoCar start. ")

########## Control ##########
# Setup Control Variable
maxDistance       =  12
backDistance      =  10       # Set 0 to Disable , Max to maxDistance 
updateFreq        = 100
enableTraceLine   = True
enableDistance    = True
enableLeftDis     = False
enableRightDis    = True
enableIRDis       = True
enableConnection  = True

# Setup Global Variable
if enableConnection:
    command       = ""


########## Import File ##########
import RPi.GPIO as gpio
import carDriver as car
import time
import datetime 
from time import sleep
if enableConnection:
    import socket
    import get_IP



########## Connection ##########
# Setup Wifi Connection (Client)
if enableConnection:
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    UDP_IP = get_IP.getBroadcastIP()
    UDP_PORT = 5005



########## Sensors ##########
# Setup GPIO
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

# Setup LED
if enableDistance:
    ledDisLeft = 24
    ledDisRight = 25
    gpio.setup(ledDisRight, gpio.OUT)
    gpio.setup(ledDisLeft, gpio.OUT)

# Setup DistanceSensor
if enableDistance:

    maxDis = maxDistance
    backDis = backDistance

    if backDis < 0:
        backDis = 0
    elif backDis > maxDis:
        backDis = maxDis

    def DisCalc(pin,tri,led):
        # set Trigger to HIGH
        gpio.output(tri, True)

        # set Trigger after 0.001ms to LOW
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
        Dis = (TimeElapsed * 34300) / 2

        if Dis > 500:
            Dis = 500
        if Dis < 5:
            Dis = 30
            
        if Dis < maxDis:
            gpio.output(led,gpio.HIGH)
        else:
            gpio.output(led,gpio.LOW)
        
        if enableDistance:
            return Dis
        else:
            return 100
    if enableLeftDis:
        echoL = 17
        triggerL = 18
        gpio.setup(triggerL, gpio.OUT)
        gpio.setup(echoL, gpio.IN)
        gpio.output(ledDisLeft, gpio.LOW)
        disL = DisCalc(echoL, triggerL, ledDisLeft)
    else:
        disL = 600

    if enableRightDis:
        echoR = 19   
        triggerR = 20 
        gpio.setup(triggerR, gpio.OUT)
        gpio.setup(echoR, gpio.IN)
        gpio.output(ledDisRight, gpio.LOW)
        disR = DisCalc(echoR, triggerR, ledDisRight)
    else:
        disR = 600
    
    if enableIRDis:
        IRPin = 26
        gpio.setup(IRPin, gpio.IN)
        
  

# Setup LineSensor
if enableTraceLine:
    readlineL = 21
    readlineM = 22
    readlineR = 23
    gpio.setup(readlineL,gpio.IN)
    gpio.setup(readlineM,gpio.IN)
    gpio.setup(readlineR,gpio.IN)

    #### About LineSensor
    # BlackLine -> 1
    # Not Black -> 0
    black = 1
    white = 0

print("Setup Finished")



########## Execution Code ##########
try:
    print("Start run Main")
    while True:
        #### Get sensor data ####
        if enableTraceLine:
            readL = gpio.input(readlineL)
            readM = gpio.input(readlineM)
            readR = gpio.input(readlineR)
            if readL:
                car.LineSensor['L'] = "black"
            else:
                car.LineSensor['L'] = "white"
            if readM:
                car.LineSensor['M'] = "black"
            else:
                car.LineSensor['M'] = "white"
            if readR:
                car.LineSensor['R'] = "black"
            else:
                car.LineSensor['R'] = "white"

        if enableDistance:
            if enableRightDis:
                disR = DisCalc(echoR, triggerR, ledDisRight)
                car.DisSensor['R'] = disR
            if enableLeftDis:  
                disL = DisCalc(echoL, triggerL, ledDisLeft)
                car.DisSensor['L'] = disL
            if enableIRDis:
                IRdist = gpio.input(IRPin)
            
        #### Car execution ####
        if enableDistance and (disR < maxDis or disL < maxDis):
            if enableRightDis and enableLeftDis:
                if disL < backDis or disR < backDis:
                    car.back()
                    if enableConnection:
                        command = "back()"

                if disL < maxDis:
                    car.turnRight(True)
                    if enableConnection:
                        command = "turnRight(True)"
                elif disR < maxDis:
                    car.turnRight(True)
                    if enableConnection:
                        command = "turnRight(True)"

                while readL != white and readM != black and readR != white:
                    if disL < maxDis:
                        car.turnRight(False)
                        if enableConnection:
                            command = "turnRight(False)"
                    else:
                        car.turnLeft(False)
                        if enableConnection:
                            command = "turnLeft(False)"
            
            else:
                if enableIRDis:
                    if IRdist == 0:
                        pass
                    else:
                        continue
                        
                if enableRightDis:
                    dis = disR
                    direction = 'right'
                else:
                    dis = disL
                    direction = 'left'
                    
                if dis < backDis:
                    car.back()
                    
                if direction == 'right':
                    car.turnRight(True)
                    if enableConnection:
                        command = "turnRight(True)"
                else:
                    car.turnLeft(True)
                    if enableConnection:
                        command = "turnLeft(True)"
                
                turn = 200
                while readL != white and readM != black and readR != white and turn:
                    if direction == 'right':
                        car.turnRight(False)
                        if enableConnection:
                            command = "turnRight(False)"
                    else:
                        car.turnLeft(False)
                        if enableConnection:
                            command = "turnLeft(False)"

        elif enableTraceLine and (readL == black or readR == black):
            if readL == black and readR == white:
                car.left()
                if enableConnection:
                    command = "left()"
            elif readL == white and readR == black:
                car.right()
                if enableConnection:
                    command = "right()"
            else:
                car.go()
                if enableConnection:
                    command = "go()"
                
        else:
            car.go()
            if enableConnection:
                command = "go()"
            
        if enableConnection:
            sock.sendto(command.encode(), (UDP_IP, UDP_PORT))
            
        sleep(1/updateFreq)


except BaseException as e:
    print("Capture Exception!")
    print(type(e), str(e))       
  
finally:
    car.stop()    
    gpio.cleanup()
    if enableConnection:
        sock.sendto("exit()".encode(), (UDP_IP, UDP_PORT))
    print("Program AutoCar Terminated!")
