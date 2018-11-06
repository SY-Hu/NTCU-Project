#! /usr/bin/python
 
import RPi.GPIO as gpio
import sys
import readchar

# input pin
ain1 = 10 
ain2 = 11
ain3 = 12
ain4 = 13

# duty cycle
motor_L1 = 0
motor_L2 = 0
motor_R1 = 0
motor_R2 = 0

# frequency
freq = 60
 
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(ain1, gpio.OUT)
gpio.setup(ain2, gpio.OUT)
gpio.setup(ain3, gpio.OUT)
gpio.setup(ain4, gpio.OUT)
 
m1 = gpio.PWM(ain1, freq)
m2 = gpio.PWM(ain2, freq)
m3 = gpio.PWM(ain3, freq)
m4 = gpio.PWM(ain4, freq)

m1.start(0)
m2.start(0)
m3.start(0)
m4.start(0)

if len(sys.argv)<=1:
    cmd = 'stop'
else:
    cmd = sys.argv[1]
 
print(cmd)
while True:
    print("=================================")
    #cmd = raw_input("Enter your command ('q' to exit):")
    cmd = readchar.readkey()
    print("COMMAND: {0}  FREQ: {1:d}".format(cmd,freq))
    if cmd == 'q':
        break 
    if cmd == 'go' or cmd =='w':
        if motor_L2 < 0:
            motor_L2 = motor_L2 + 10
        else:
            motor_L1 = motor_L1 + 10
        if motor_R2 < 0:
            motor_R2 = motor_R2 + 10
        else:
            motor_R1 = motor_R1 + 10
    elif cmd == 'stop' or cmd ==' ':
        motor_L1 = 0
        motor_L2 = 0
        motor_R1 = 0
        motor_R2 = 0
    elif cmd == 'back' or cmd =='s':
        if motor_L1 > 0 :
            motor_L1 = motor_L1 - 10
        else: 
            motor_L2 = motor_L2 + 10
        if motor_R1 > 0 :
            motor_R1 = motor_R1 - 10
        else:
            motor_R2 = motor_R2 + 10
    elif cmd == 'left' or cmd =='a':
        motor_L1 = motor_L1 + 10
        motor_R2 = motor_R2 - 10
    elif cmd == 'right' or cmd =='d':
        motor_L2 = motor_L2 + 10
        motor_R1 = motor_R1 - 10
    elif cmd =='r':
        freq = freq + 2
    elif cmd =='f':
        freq = freq - 2
    else:
        motor_L1 = 0
        motor_L2 = 0
        motor_R1 = 0
        motor_R2 = 0
        freq = 60
    
    #protect motor
    if motor_L1 > 100:
        motor_L1 = 100
    elif motor_L1 < 0:
        motor_L1 = 0

    if motor_L2 > 100:
        motor_L2 = 100
    elif motor_L2 < 0:
        motor_L2 = 0    
   
    if motor_R1 > 100:
        motor_R1 = 100
    elif motor_R1 < 0:
        motor_R1 = 0

    if motor_R2 > 100:
        motor_R2 = 100
    elif motor_R2 < 0:
        motor_R2 = 0

    print(" L1:",motor_L1," L2:",motor_L2," R1:",motor_R1," R2:",motor_R2)
    #set to motor
    m1.ChangeDutyCycle(motor_R1)
    m2.ChangeDutyCycle(motor_R2)
    m3.ChangeDutyCycle(motor_L1)
    m4.ChangeDutyCycle(motor_L2)

gpio.cleanup()
