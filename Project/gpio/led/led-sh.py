import RPi.GPIO as GPIO
import subprocess
from time import sleep

while True: 
    subprocess.call("./openLED.sh")
    print "Led on by shell"
    sleep(1)
    subprocess.call("./closeLED.sh")
    print "Led off by shell"
    sleep(1)
