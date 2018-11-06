#! /usr/bin/python
import RPi.GPIO as gpio
import sys

# define func to calc turn ratio
def turnCircle( radius ):
    return (radius+10.5)/radius

# input pin
ain1 = 29 
ain2 = 7
ain3 = 33
ain4 = 13

# duty cycle
motor = [0,0,0,0] # L1,L2 , R1,R2

# turn ratio
ratio = 0.0

# speed step and turn step
ss = 0 # back -2 ~ 2 front
ts = 0 # left -1 ~ 1 right
 
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(ain1, gpio.OUT)
gpio.setup(ain2, gpio.OUT)
gpio.setup(ain3, gpio.OUT)
gpio.setup(ain4, gpio.OUT)

# set to gpio 
m1 = gpio.PWM(ain1, 30)
m2 = gpio.PWM(ain2, 30)
m3 = gpio.PWM(ain3, 30)
m4 = gpio.PWM(ain4, 30)

m1.start(0)
m2.start(0)
m3.start(0)
m4.start(0)

if len(sys.argv)<=1:
    cmd = 'stop'
else:
    cmd = sys.argv[1]

# get command and set to ss,ts 
print(cmd)
while True:
    
    cmd = raw_input("Enter your command ('q' to exit):")
    if cmd == 'q':
        break 
    if cmd == 'go' or cmd =='w':
        ss = ss + 1
    elif cmd == 'stop' or cmd ==' ':
        ss = 0
        ts = 0
    elif cmd == 'back' or cmd =='s':
        ss = ss - 1
    elif cmd == 'left' or cmd =='a':
        ts = ts - 1
    elif cmd == 'right' or cmd =='d':
        ts = ts + 1
    else:
        ss = 0
        ts = 0
    
    # set ss,ts upper,lower bound
    if ss > 2:
        ss = 2
    elif ss < -2:
        ss = -2

    if ts > 1:
        ts = 1
    if ts < -1:
        ts = -1

    # ss set to motor
    if ss == 0: 
        motor[0:3] = [0,0,0,0]
    elif ss == 1:
        motor[0:3] = [40,0,40,0]
    elif ss == 2:
        motor[0:3] = [70,0,70,0]
    elif ss == -1:
        motor[0:3] = [0,40,0,40]
    elif ss == -2:
        motor[0:3] = [0,70,0,70]
    
    # ts set to motor
    # Tank mode
    if ts == 1 or ts == -1:
       ratio = turnCircle(0.0)
    else:
        ratio = 1.0
    
    if ss != 0:
        if ts < 0:
            motor[0] = motor[0] * ratio
            motor[1] = motor[1] * ratio
        elif ts > 0:
            motor[2] = motor[2] * ratio
            motor[3] = motor[3] * ratio 
        else:
            for i in range(4):
                motor[i] = motor[i]    
    else:
        if ts < 0:
            motor[0:3] = [40,0,0,40]
        elif ts > 0:
            motor[0:3] = [0,40,40,0]
        else:
            motor[0:3] = [0,0,0,0]


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
