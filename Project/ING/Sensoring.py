#! /usr/bin/python

#########################################
# NTCU Computer Science 
# Project 107 - 08 
# Program : Car Sensoring
#
#########################################

print("NTCU Computer Science Project 107-08")
print("Program : Car Sensoring")
print("Program start. ")

########## Control ##########
# Setup Control Variable
sensorFreq        =  1
enableDHT11       = True
enableGPS         = False
enableQuery2SQL   = False
displayMessage    = True

########## Import File ##########
import RPi.GPIO as gpio
import time
import datetime
from time import sleep
if enableDHT11:
    import dht11
if enableQuery2SQL:
    import MySQLdb
if enableGPS:
    import socket
    from gps3 import gps3  



########## Connection ##########
# Setup MySQL connection
if enableQuery2SQL:
    db = MySQLdb.connect(host="car.leafu.one", port=3307 , user='nopass', passwd='bH5cpZ8VOg4wCPX!', db="test")
    cur = db.cursor()
    print("DataBase Connect.")

########## Sensors ##########
# Setup GPIO
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

# Setup DHT11
if enableDHT11:
    th = dht11.DHT11( pin = 16 )
    
    temperature = 0
    humidity = 0
    

# Setup GPS
if enableGPS:
    gps_socket = gps3.GPSDSocket()
    data_stream = gps3.DataStream()
    gps_socket.connect()
    gps_socket.watch()
    
    altitude = 0
    latitude = 0
    longitude = 0

print("Setup Finished")



########## Execution Code ##########
try:
    while True:
        #### Humidity Temperature ####
        if enableDHT11:
            htread = th.read()
            
            if htread.is_valid():   
                temperature = htread.temperature
                humidity = htread.humidity
                
                if displayMessage:
                    print("Temperature: %d C" % temperature)
                    print("Humidity: %d %%" % humidity)

        #### GPS ####
        if enableGPS:    
            for new_data in gps_socket:
                if new_data:
                    data_stream.unpack(new_data)
                    
                    altitude = data_stream.TPV['alt']
                    latitude = data_stream.TPV['lat']
                    longitude = data_stream.TPV['lon']
                    
                    if displayMessage:
                        print('Altitude = ', altitude)
                        print('Latitude = ', latitude)
                        print('Longitude = ', longitude)
                break

        #### Query to SQL ####
        if enableGPS:        
            # Execute insert gps sql
            query = ("INSERT INTO gps (gpslat,gpslng,username) VALUES (%s,%s,%s)")
            data = (latitude, longitude, 'car')
            cur.execute(query, data)
            db.commit()
            # Execute insert sensor sql
            querye = ("INSERT INTO sensor (gpslat, gpslng, temperature, humidity, username) VALUES (%s,%s,%s,%s,%s)")
            sen = (latitude, longitude, temperature, humidity , 'car')
            cur.execute(querye, sen)
            db.commit()   

        sleep(1/sensorFreq)

except BaseException as e:
    print("Capture Exception!")
    print(type(e), str(e))       
  
finally:   
    gpio.cleanup()
    print("Program Car Sensoring Terminated!")