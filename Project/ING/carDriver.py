#! /usr/bin/python

#########################################
# NTCU Computer Science 
# Project 107 - 08 
# Program : Car Driver
# 
#########################################

########## Control ##########
# Setup Control Variable
turnPercent       =  55
goSpeed           =  55
slowSpeed         =  55
turnTime          =  2
backTime          =  0.5
enableConnection  = False

# Setup Global Variable
isStopped  = False

# Setup DashBoard Variable
action     = "NULL" 
DisSensor  = {'L':0, 'R':0}
LineSensor = {'L':"white", 'M':"white", 'R':"white"}



########## Import File ##########
import RPi.GPIO as gpio
from time import sleep



########## Setup General ##########
# Setup GPIO
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

# Setup LED
ledLeft = 7
ledRight = 12
gpio.setup(ledRight, gpio.OUT)
gpio.setup(ledLeft, gpio.OUT)


########## Setup Car ##########
# Define input pin
ain1 = 5 
ain2 = 4
ain3 = 13
ain4 = 27

# Set default duty cycle
motor = [0,0,0,0] # L1,L2 , R1,R2
 
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

# Define function to command the car
def start():
    motor[0:3] = [55,0,55,0]
    global action
    action = "Start Motor"
    exe()
    # = False
    sleep(0.001)

def go():
    '''if isStopped:
        print("Command: START     ", end='')
        start()'''
    motor[0:3] = [goSpeed,0,goSpeed,0]
    global action
    action = "Go"
    gpio.output(ledLeft,gpio.LOW)
    gpio.output(ledRight,gpio.LOW)
    exe()

def stop():
    motor[0:3] = [0,0,0,0]
    global action
    action = "Stop"
    gpio.output(ledLeft,gpio.HIGH)
    gpio.output(ledRight,gpio.HIGH)
    #isStopped = True
    exe()

def back():
    motor[0:3] = [0,goSpeed,0,goSpeed]
    global action
    action = "Back"
    gpio.output(ledLeft,gpio.LOW)
    gpio.output(ledRight,gpio.LOW)
    exe()
    sleep(backTime)

def turnRight(doTime):
    motor[0:3] = [turnPercent,0,0,turnPercent]
    global action
    action = "Right Turn"
    gpio.output(ledLeft,gpio.LOW)
    gpio.output(ledRight,gpio.HIGH)
    exe()
    if doTime:
        sleep(turnTime)

def right():
    '''if isStopped:
        print("Command: START     ", end='')
        start()'''
    motor[0:3] = [turnPercent,0,0,0]
    global action
    action = "Right"
    gpio.output(ledLeft,gpio.LOW)
    gpio.output(ledRight,gpio.HIGH)
    exe()

def turnLeft(doTime):
    motor[0:3] = [0,turnPercent,turnPercent,0]
    global action
    action = "Left Turn"
    gpio.output(ledLeft,gpio.HIGH)
    gpio.output(ledRight,gpio.LOW)
    exe()
    if doTime:
        sleep(turnTime)

def left():
    '''if isStopped:
        print("Command: START     ", end='')
        start()'''
    motor[0:3] = [0,0,turnPercent,0]
    global action
    action = "Left"
    gpio.output(ledLeft,gpio.HIGH)
    gpio.output(ledRight,gpio.LOW)
    exe()

def slowGo():
    '''if isStopped:
        print("Command: START     ", end='')
        start()'''
    motor[0:3] = [slowSpeed,0,slowSpeed,0]
    global action
    action="Go Slowly"
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

    #set to motor
    m1.ChangeDutyCycle(motor[0])
    m2.ChangeDutyCycle(motor[1])
    m3.ChangeDutyCycle(motor[2])
    m4.ChangeDutyCycle(motor[3])
    
    dashboard()
    
    if enableConnection:
        sock.sendto(action.encode(), (UDP_IP, UDP_PORT))
    
'''
class DashBoard:
    def __init__(self):
'''    


########## Setup Dashboard ##########
# Function to Display dashboard
def dashboard():
    global action
    print('  DistanceL     DistanceR')
    print("    {0:3.2f}       {1:3.2f}".format(DisSensor['L'],DisSensor['R'])) 
    print('  LineL    LineM    LineR')
    print("  {0}    {1}    {2}".format(LineSensor['L'],LineSensor['M'],LineSensor['R']))
    print("  Action = {0}".format(action))
    print("  Motor  = [ {0}, {1}, {2}, {3}]".format(motor[0],motor[1],motor[2],motor[3]))
    print('===========================')

