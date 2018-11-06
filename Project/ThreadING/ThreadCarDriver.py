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

########## Car Driver ##########
class CarDriver(threading.Thread):
    def __init__(self,led_L=19,led_R=20,inp1=ain1,inp2=ain2,inp3=ain3,inp4=ain4,turnSp=turnSpeed,goSp=goSpeed,freq=1000):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.command = "Stop"
        self.cmd_change_ori = 10
        self.cmd_change = 0
        self.wait = 0
        self.freq = freq
        self.turnSpeed = turnSp
        self.goSpeed = goSp
        self.led_L = led_L
        self.led_R = led_R
        self.ain_pin = [inp1,inp2,inp3,inp4]
        self.motor = []
        self.motor_PWM = [0,0,0,0]
        if not self.led_L == None and not self.led_R == None:
            GPIO.setup(self.led_L, GPIO.OUT)
            GPIO.setup(self.led_R, GPIO.OUT)
        for i in self.ain_pin:
            GPIO.setup(i, GPIO.OUT)
            self.motor.append(GPIO.PWM(i, pwm_frequence))
        for motors in self.motor:
            motors.start(0)

    def run(self):
        while(not self._stop_event.is_set()):
            if self.cmd_change == 0:
                self.cmd_change = self.cmd_change_ori
                
                ##### Set car motor frequency
                if self.command == 'Go':
                    self.motor_PWM[0:3] = [self.goSpeed,0,self.goSpeed,0]
                elif self.command == 'Stop': 
                    self.motor_PWM[0:3] = [0,0,0,0]
                elif self.command == 'Back':
                    self.motor_PWM[0:3] = [0,self.goSpeed,0,self.goSpeed]
                elif self.command == 'Left':
                    self.motor_PWM[0:3] = [0,0,self.turnSpeed,0]
                elif self.command == 'Right':
                    self.motor_PWM[0:3] = [self.turnSpeed,0,0,0]
                elif self.command == 'TurnLeft':
                    self.motor_PWM[0:3] = [0,self.turnSpeed,self.turnSpeed,0]
                elif self.command == 'TurnRight':
                    self.motor_PWM[0:3] = [self.turnSpeed,0,0,self.turnSpeed]
                
                ##### Set direction LED
                if not self.led_L == None and not self.led_R == None: 
                    if self.command == 'Left' or self.command == 'TurnLeft':
                        GPIO.output(self.led_L,GPIO.HIGH)
                        GPIO.output(self.led_R,GPIO.LOW)
                    elif self.command == 'Right' or self.command == 'TurnRight':
                        GPIO.output(self.led_L,GPIO.LOW)
                        GPIO.output(self.led_R,GPIO.HIGH)
                    else:
                        GPIO.output(self.led_L,GPIO.LOW)
                        GPIO.output(self.led_R,GPIO.LOW)
                
                ##### Check motor frequency
                for motor_freq in self.motor_PWM:
                    if motor_freq > 100:
                        motor_freq = 100
                    elif motor_freq < 0:
                        motor_freq = 0
                
                for no in range(4):
                    self.motor[no].ChangeDutyCycle(self.motor_PWM[no])
                
                if self.wait > 0:
                    self.wait = self.wait-(1/self.freq) 
                    if self.wait > 0:
                        time.sleep(self.wait)
                    self.wait = 0
               
            elif self.cmd_change < 0:
                self.cmd_change = 0
            else:    
                self.cmd_change = self.cmd_change - 1   
                
            time.sleep(1/self.freq)   
            
    def assign(self,command,time=0):
        self.cmd_change = 0
        self.command = command
        if time > 0:
            self.wait = time
            
    def status(self):
        print("[CarDriver] Command=\'%s\' Motor=[%3d,%3d,%3d,%3d]"%(self.command,self.motor_PWM[0],self.motor_PWM[1],self.motor_PWM[2],self.motor_PWM[3]))

    def stop(self):
        self._stop_event.set()
    
    def __del__(self):
        self.motor_PWM[0:3] = [0,0,0,0]
        for no in range(4):
            self.motor[no].ChangeDutyCycle(0)