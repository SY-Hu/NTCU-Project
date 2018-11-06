#! /usr/bin/python

#########################################
# NTCU Computer Science 
# Project 107 - 08 
# Program : Test Car Driver
# 
#########################################

########## Basic Setup ##########
import ThreadCarDriver
import threading
from time import sleep


threadList = []
car = ThreadCarDriver.CarDriver()
threadList.append(car)
try:
    pass
    car.start()
except BaseException as e:
    print("[CarTest] Capture Exception while starting threads!")
    print(type(e), str(e))
    
try:
    while True:
        command = input("[CarTest] Input command: ")
        if command == 'Go' or \
           command == 'Stop' or \
           command == 'Back' or \
           command == 'Left' or \
           command == 'Right' or \
           command == 'TurnLeft' or \
           command == 'TurnRight':
            car.assign(command)
            print("[CarTest] Get command :",command)
        elif command == 'Quit' or \
             command == 'Exit':
            break
        else:
            print("[CarTest] Unknown command. Enter Exit or Quit to exit.")
except BaseException as e:
    print("[CarTest] Capture Exception while starting threads!")
    print(type(e), str(e))
finally:
    for threads in threadList:
        threads.stop()
        threads.join()
    print("[CarTest] Program End!")
    
    

