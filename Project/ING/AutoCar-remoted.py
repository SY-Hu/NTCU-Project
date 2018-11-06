#! /usr/bin/python

#########################################
# NTCU Computer Science 
# Project 107 - 08 
# Program : Auto TraceLine Car
#            with Wifi Sender
#########################################

print("NTCU Computer Science Project 107-08")
print("Program : Auto Car with Wifi Reciever")
print("Program AutoCar start. ")

########## Control ##########
# Setup Control Variable
waitForCommandMax =  500
updateFreq        = 2000
enableConnection  = True

# Setup Global Variable
if enableConnection:
    command       = "null()"
    receive       = ""
    nullReceive   = waitForCommandMax


########## Import File ##########
import RPi.GPIO as gpio
import carDriver as car
import time
import datetime 
from time import sleep
if enableConnection:
    import socket



########## Connection ##########
# Setup Wifi Connection (Client)
if enableConnection:
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    UDP_PORT = 5005
    sock.bind(('', UDP_PORT))



########## Sensors ##########
# Setup GPIO
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

print("Setup Finished")



########## Execution Code ##########
try:
    print("Start run Main")
    while True:
        #### Get Remote command ####
        receive = sock.recv(4096)
        if not receive:
            nullReceive = nullReceive - 1
            print("No command receive! Countdown: %d" % nullReceive)
        else:
            command = receive.decode()
            print("Command = %s" % command)
            nullReceive = waitForCommandMax
            
        #### Car execution ####
        if nullReceive != 0:
            if command == 'go()':
                car.go()
            elif command == 'left()':
                car.left()
            elif command == 'right()':
                car.right()
            elif command == 'back()':
                car.back()
            elif command == 'stop()':
                car.stop()
            elif 'turnRight' in command:
                if 'True' in command:
                    car.turnRight(True)
                elif 'false' in command:
                    car.turnRight(False)
            elif 'turnLeft' in command:
                if 'True' in command:
                    car.turnLeft(True)
                elif 'false' in command:
                    car.turnLeft(False)
            elif command == 'exit()':
                break
        else:
            print("Can't receive command!")
            car.stop()
            break
        
        sleep(1/updateFreq)


except BaseException as e:
    print("Capture Exception!")
    print(type(e), str(e))       
  
finally:
    car.stop()    
    gpio.cleanup()
    print("Program AutoCar Terminated!")
