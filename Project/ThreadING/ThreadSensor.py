#! /usr/bin/python

#########################################
# NTCU Computer Science 
# Project 107 - 08 
# Program : Car Sensoring Thread
#
#########################################

print("NTCU Computer Science Project 107-08")
print("Program : Car Sensoring Thread")
print("Program start. ")

########## Basic setup ##########
import threading
import RPi.GPIO as GPIO
import time
#import datetime
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

########## DistanceSensor ##########
class DistanceSensor(threading.Thread):
    def __init__(self,echo,trig,led=None,ir=None,freq=1000,maxDis=10):
        print("[Distance] Thread start.\n")
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.value = 0
        self.echo = echo
        self.trig = trig
        self.led = led
        self.ir = ir
        self.freq = freq
        self.maxDis = maxDis
        GPIO.setup(trig, GPIO.OUT)
        GPIO.setup(echo, GPIO.IN)
        if not self.led == None:
            GPIO.setup(self.led, GPIO.OUT)
            GPIO.output(self.led, GPIO.LOW)
        if not self.ir == None:
            GPIO.setup(self.ir, GPIO.IN)
        
    def run(self): 
        while(not self._stop_event.is_set()):
            value = self.DisCalc(self.echo,self.trig)
            #print("[Distance] Distance in thread : %3.3f"%(value))
            if value < self.maxDis and not self.ir == None:
                IRdist = GPIO.input(self.ir)
                if IRdist == 1: # ultrasonic detect wrong distance
                    print("[Distance] Wrong distance : %3.3f \n" % value)
                else:
                    self.value = value
            else:
                self.value = value
            if not self.led == None:
                if self.value < self.maxDis :
                    GPIO.output(self.led, GPIO.HIGH)
                else:
                    GPIO.output(self.led, GPIO.LOW)
            time.sleep(1/self.freq)
               
    def DisCalc(self,pin,tri):
        # set Trigger to HIGH
        GPIO.output(tri, True)
        # set Trigger after 0.001ms to LOW
        time.sleep(0.00001)
        GPIO.output(tri, False)
        StartTime = time.time()
        StopTime = time.time()
        # save StartTime
        while GPIO.input(pin) == 0:
            StartTime = time.time()
        # save time of arrival
        while GPIO.input(pin) == 1:
            StopTime = time.time()
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        if TimeElapsed <= 0:
            TimeElapsed = 1
            print("[Distance] Pin ",pin ,' time too small.')
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        return (TimeElapsed * 34300) / 2
        
    def stop(self):
        self._stop_event.set()   
    
    def __del__(self):
        if not self.led == None:
            GPIO.output(self.led, GPIO.LOW)
        print("[Distance] Thread End\n")

########## GPS ##########
class GPSMeter(threading.Thread):
    def __init__(self,freq=1000):
        import socket
        from gps3 import gps3 
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.displayMessage = True
        self.old = 0
        self.freq = freq
        self.altitude = 0
        self.latitude = 0
        self.longitude = 0
        self.value = {'altitude':0,'latitude':0,'longitude':0}
        try:
            self.gps_socket = gps3.GPSDSocket()
            self.data_stream = gps3.DataStream()
            self.gps_socket.connect()
            self.gps_socket.watch()
            print("[GPS ] GPS setup finished.")
        except BaseException as e:
            print("[GPS ] Capture Exception while setup! ")
            print(type(e), str(e))
            exit(1)
    
    def run(self):
        while(not self._stop_event.is_set()):
            for new_data in self.gps_socket:
                if new_data:
                    self.data_stream.unpack(new_data)
                    self.old = 0
                        
                    self.altitude = self.data_stream.TPV['alt']
                    self.latitude = self.data_stream.TPV['lat']
                    self.longitude = self.data_stream.TPV['lon']
                    self.value['altitude'] = self.altitude
                    self.value['latitude'] = self.latitude
                    self.value['longitude'] = self.longitude
                        
                    if self.displayMessage:
                        print('Altitude = ', self.altitude)
                        print('Latitude = ', self.latitude)
                        print('Longitude = ', self.longitude)
                else:
                    self.old = self.old +1
                if self._stop_event.is_set():
                    break
            time.sleep(1/self.freq)
            
    def stop(self):
        self._stop_event.set() 
           
########## LineSensor ##########
class LineSensor(threading.Thread):
    def __init__(self,pin,freq=1000):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.pin = pin
        self.freq = freq
        self.value = "white"
        GPIO.setup(pin,GPIO.IN)
        self.black = 1   # BlackLine -> 1
        self.white = 0   # Not Black -> 0
    
    def run(self):
        while(not self._stop_event.is_set()):
            read = GPIO.input(self.pin)
            if read == 1:
                self.value = "black"
            else:
                self.value = "white"
            time.sleep(1/self.freq)
 
    def stop(self):
        self._stop_event.set()  

########## DHT11 ##########
class DHT11Sensor(threading.Thread): 
    def __init__(self,pin,freq=10):
        import dht11
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.freq = freq
        self.displayMessage = True
        self.th = dht11.DHT11(pin)
        self.pin = pin
        self.value = {'temperature':0,'humidity':0}
        self.temperature = 0
        self.humidity = 0
        self.ready = False 
    
    def run(self):
        while(not self._stop_event.is_set()):
            htread = self.th.read()
            if htread.is_valid():
                self.ready = True
                self.temperature = htread.temperature
                self.humidity = htread.humidity
                self.value['temperature'] = self.temperature
                self.value['humidity'] = self.humidity
                if self.displayMessage:
                    print("[DHT11] Temperature: %d C Humidity: %d %%" % (self.temperature,self.humidity))
        time.sleep(1/self.freq)
        
    def stop(self):
        self._stop_event.set()
        
########## Light ########## (MCP3008)
class LightSensor(threading.Thread):
    def __init__(self,freq=10,channel=0,upper=20,lower=100):
        import spidev
        import os
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
        self.freq = freq
        self.upper = upper
        self.lower = lower
        self.value = "light"
        self.channel = channel
    
    def readADC(self,ch):
        if ((ch > 7) or (ch < 0)):
           return -1
        adc = self.spi.xfer2([1,(8+ch)<<4,0])
        data = ((adc[1]&3)<<8) + adc[2]
        return data
    
    def run(self):
        while(not self._stop_event.is_set()):
            lightData = self.readADC(self.channel)
            #print("[Light] Sensor Value =",lightData)
            if self.value == 'dark' and lightData < self.lower:
                self.value = "light"  # Enviroment is light , close light.
            if self.value == 'light' and lightData > self.upper:
                self.value = "dark" # Enviroment is dark , open light.
            time.sleep(1/self.freq)
    
    def stop(self):
        self._stop_event.set()
