#! /usr/bin/python
import RPi.GPIO as gpio
import sys
import time
import socket
from time import sleep

print("AutoCar Socket Client - Bluetooth ver.")
print("Program start. ")

# Setup Global Variable
maxDistance = 10
enableTraceLine = True
isStopped = True
turnPercent = 40
enableDistance = True

# Setup Connection (Server)
hostMACAddress = 'B8:27:EB:E7:15:8D'
port = 22
backlog = 1
size = 1024
s = socket.socket(socket.AF_BLUETOOTH,socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((hostMACAddress,port))
s.listen(backlog)

# Setup GPIO
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)

# Setup LED
ledLeft = 23
ledRight = 24
ledDisLeft = 21
ledDisRight = 22
gpio.setup(ledRight, gpio.OUT)
gpio.setup(ledLeft, gpio.OUT)
gpio.setup(ledDisRight, gpio.OUT)
gpio.setup(ledDisLeft, gpio.OUT)

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
    
    if enableDistance:
        return distance
    else:
        return 100

# Set up LineSensor

readlineL = 29
readlineM = 31
readlineR = 32

gpio.setup(readlineL,gpio.IN)
gpio.setup(readlineM,gpio.IN)
gpio.setup(readlineR,gpio.IN)


# Define function to command the car
def start():
    motor[0:3] = [55,0,55,0]
    exe()
    isStopped = False
    sleep(0.001)

def go():
    if isStopped:
        print("Command: START     ", end='')
        start()
    motor[0:3] = [30,0,30,0]
    gpio.output(ledLeft,gpio.LOW)
    gpio.output(ledRight,gpio.LOW)
    exe()

def stop():
    motor[0:3] = [0,0,0,0]
    gpio.output(ledLeft,gpio.HIGH)
    gpio.output(ledRight,gpio.HIGH)
    isStopped = True
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
    if isStopped:
        print("Command: START     ", end='')
        start()
    motor[0:3] = [turnPercent,0,0,0]
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
    if isStopped:
        print("Command: START     ", end='')
        start()
    motor[0:3] = [0,0,turnPercent,0]
    gpio.output(ledLeft,gpio.HIGH)
    gpio.output(ledRight,gpio.LOW)
    exe()

def slowGo():
    if isStopped:
        print("Command: START     ", end='')
        start()
    motor[0:3] = [30,0,30,0]
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
    client,address = s.accept()
    while True:
        data = client.recv(size)

        gpio.output(ledDisLeft,gpio.LOW)
        gpio.output(ledDisRight,gpio.LOW)
  
        #UI
        print('DisL  LineL  LineM  LineR  DisR  ')
        print('{0:3.2f}  {1:d}      {2:d}     {3:d}    {4:3.2f}'.format(distanceL,readL,readM,readR,distanceR))





        if data == "GO":
            print("Command: GO        ", end='')
            go()
        elif data == "START":
            print("Command: START     ", end='')
            start()
        elif data == "LEFT":
            # Go Left
            print("Command: LEFT      ", end='')
            left()
        elif data == "RIGHT":
            # Go Right
            print("Command: RIGHT     ", end='')
            right()
        elif data == "TURN RIGHT":
            print("Command: TURN RIGHT", end='')
            turnRight()
        elif data == "TURN LEFT":
            print("Command: TURN LEFT ", end='')
            turnLeft()
        elif data == "SKIP":
            # All No Line
            #stop()
            print("Command: SKIP")
        elif data == "BACK":
            # All On Line
            print("Command: BACK      ", end='')
            back()
        elif data == "STOP":
            # All On Line
            print("Command: STOP      ", end='')
            stop()
        elif data == "SLOW GO":
            # All On Line
            print("Command: STOP      ", end='')
            stop()
        elif data == "EXIT":
            # All On Line
            print("Command: EXIT      ", end='')
        '''elif data == "GO":
		    # distanceL < maxDistance or distanceR < maxDistance:
            # Led Control
            if distanceL < maxDistance:
                gpio.output(ledDisLeft,gpio.HIGH)
            if distanceR < maxDistance:
                gpio.output(ledDisRight,gpio.HIGH)

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
            sleep(0.2)'''
        else:
            print("Command: Slow Go   ", end='')
            slowGo()
        
        # UI status
        '''if readL == 0 and readM == 0 and readR == 0:
            print("Car can't find line.")
        elif readL == 1 and readM == 1 and readR == 1:
            print("Car is all on line.")
        else:
            print(" ")'''


        print('==========================')


except:    
    print("Command: FORCE STOP ", end='')
    stop()
    gpio.cleanup()
