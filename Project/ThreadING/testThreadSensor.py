#! /usr/bin/python

#########################################
# NTCU Computer Science 
# Project 107 - 08 
# Program : Test Car Driver
# 
#########################################

########## Basic Setup ##########
import ThreadSensor
import threading
import time
from time import sleep

freq           =  10

threads        =  []

enableDistance =  True
enableLine     = False
enableDHT11    = False
enableGPS      = False
enableLight    = False

if enableDistance:
    Distance = ThreadSensor.DistanceSensor(echo=16,trig=17,ir=13,led=18)
    threads.append(('Distance',Distance))
        
if enableLine:
    Line_L = ThreadSensor.LineSensor(pin=4)
    Line_R = ThreadSensor.LineSensor(pin=6)
    threads.append(('Line_L',Line_L))
    threads.append(('Line_R',Line_R))

if enableDHT11:
    Dht11 = ThreadSensor.DHT11Sensor(pin=12)
    threads.append(('Dht11',Dht11))

if enableGPS:
   Gps = ThreadSensor.GPSMeter()
   threads.append(('Gps',Gps))
   
if enableLight:
    Light =  ThreadSensor.LightSensor()
    threads.append(('Light',Light))
   
try:
    for thread in threads:
        thread[1].start()
except BaseException as e:
    print("[TestSensor] Capture Exception while starting threads!")
    print(type(e), str(e))

try:
    while True:
        if enableDistance:
            print("[TestSensor] Distance : ",Distance.value)
            print("[TestSensor] Distance is alive?",Distance.is_alive())
        
        if enableLine:
            print("[TestSensor] Line_L   : ",Line_L.value)
            print("[TestSensor] Line_R   : ",Line_R.value)
        
        if enableDHT11:
            print("[TestSensor] dht11    : ",Dht11.value)
            
        if enableGPS:
            print("[TestSensor] Gps      : ",Gps.value)
            
        if enableLight:
            print("[TestSensor] Light    : ",Light.value)
        
        #for thread in threads:
        #    print("[TestSensor] In for %8s : "%(thread[0]),thread[1].value)
            
        
        
        time.sleep(1/freq)
        
except BaseException as e:
    print("[TestSensor] Capture Exception while Executing threads!")
    print(type(e), str(e))

finally:
    for thread in threads:
        thread[1].stop()
        thread[1].join()
