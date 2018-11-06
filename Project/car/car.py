#! /usr/bin/python
 
import RPi.GPIO as gpio
import sys

ain1 = 11 
ain2 = 12
ain3 = 13
ain4 = 16
 
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(ain1, gpio.OUT)
gpio.setup(ain2, gpio.OUT)
gpio.setup(ain3, gpio.OUT)
gpio.setup(ain4, gpio.OUT)
 
if len(sys.argv)<=1:
    cmd = 'stop'
else:
    cmd = sys.argv[1]
 
print(cmd)
while True:
    cmd = raw_input("Enter your command ('q' to exit):")
    if cmd == 'q':
        break 
    if cmd == 'go' or cmd =='g':
        gpio.output(ain1, True)
        gpio.output(ain2, False)
        gpio.output(ain3, True)
        gpio.output(ain4, False)
    elif cmd == 'stop' or cmd =='s':
        gpio.output(ain1, False)
        gpio.output(ain2, False)
        gpio.output(ain3, False)
        gpio.output(ain4, False)
    elif cmd == 'back' or cmd =='b':
        gpio.output(ain1, False)
        gpio.output(ain2, True)
        gpio.output(ain3, False)
        gpio.output(ain4, True)
    elif cmd == 'left' or cmd =='l':
        gpio.output(ain1, True)
        gpio.output(ain2, False)
        gpio.output(ain3, False)
        gpio.output(ain4, True)
    elif cmd == 'right' or cmd =='r':
        gpio.output(ain1, False)
        gpio.output(ain2, True)
        gpio.output(ain3, True)
        gpio.output(ain4, False)
    else:
        gpio.output(ain1, False)
        gpio.output(ain2, False)
        gpio.output(ain3, False)
        gpio.output(ain4, False)
gpio.cleanup()
