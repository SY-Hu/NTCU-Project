#! /usr/bin/python

#########################################
# NTCU Computer Science 
# Project 107 - 08 
# Program : Car Driver
# 
#########################################

########## Control ##########
# Setup Car Variable
turnSpeed         =  50
goSpeed           =  50

# Setup Motor Variable
pwm_frequence     =  30
ain1              =  27 
ain2              =  22
ain3              =  23
ain4              =  24

########## Basic Setup ##########
import RPi.GPIO as GPIO
import time
import threading
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

########## Define Variable ##########
command = "Stop"
ain_pin = [ain1,ain2,ain3,ain4]
motor = []
motor_PWM = [0,0,0,0]
for i in ain_pin:
    GPIO.setup(i, GPIO.OUT)
    motor.append(GPIO.PWM(i, pwm_frequence))
for motors in motor:
    motors.start(0)
motorNo = {'Ain1':0,'Ain2':1,'Ain3':2,'Ain4':3}
########## Motor Driver ##########
try:
    while True:
        print("[TestMotor] To set indivial motor, input 'Set Ain(1/2/3/4) (0~100).")
        command = input("[TestMotor] Input command: ")
        ##### Set car motor frequency
        if command == 'Go':
            motor_PWM[0:3] = [goSpeed,0,goSpeed,0]
        elif command == 'Stop': 
            motor_PWM[0:3] = [0,0,0,0]
        elif command == 'Back':
            motor_PWM[0:3] = [0,goSpeed,0,goSpeed]
        elif command == 'Left':
            motor_PWM[0:3] = [0,0,turnSpeed,0]
        elif command == 'Right':
            motor_PWM[0:3] = [turnSpeed,0,0,0]
        elif command == 'TurnLeft':
            motor_PWM[0:3] = [0,turnSpeed,turnSpeed,0]
        elif command == 'TurnRight':
            motor_PWM[0:3] = [turnSpeed,0,0,turnSpeed]
        elif command == 'Exit' or command == 'Quit':
            break
        elif 'Set' in command:
            commandSplit = command.split(' ')
            motor_PWM[motorNo[commandSplit[1]]] = int(commandSplit[2])
            
        
        ##### Check motor frequency
        for motor_freq in motor_PWM:
            if motor_freq > 100:
                motor_freq = 100
            elif motor_freq < 0:
                motor_freq = 0
        
        for no in range(4):
            motor[no].ChangeDutyCycle(motor_PWM[no])
            
        print("[TestMotor] Command=\'%s\' Motor=[%3d,%3d,%3d,%3d]"%(command,motor_PWM[0],motor_PWM[1],motor_PWM[2],motor_PWM[3]))
            
except BaseException as e:
    print("Capture Exception!")
    print(type(e), str(e))       
    
finally:
    motor_PWM[0:3] = [0,0,0,0]
    for no in range(4):
        motor[no].ChangeDutyCycle(0)


