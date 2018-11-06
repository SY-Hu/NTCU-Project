#! /usr/bin/python

#########################################
# NTCU Computer Science 
# Project 107 - 08 
# Program : Test ThreadCommunication Upload
# 
#########################################

########## Basic Setup ##########
import ThreadCommunication
import threading
import time
from time import sleep

freq           =    2
threads        =   []
trueData       = True

if trueData:
    import ThreadSensor

Upload = ThreadCommunication.UploadData()
threads.append(('Upload',Upload))

if trueData:
    Dht11 = ThreadSensor.DHT11Sensor(pin=12)
    threads.append(('Dht11',Dht11))

    Gps = ThreadSensor.GPSMeter()
    threads.append(('Gps',Gps))
   
try:
    for thread in threads:
        thread[1].start()
except BaseException as e:
    print("[TestSensor] Capture Exception while starting threads!")
    print(type(e), str(e))

    
########## Main ##########
try:
    while True:
        if trueData == True:
            if not Gps.value['latitude'] == 0 and not Gps.value['longitude'] == 0:
                lat = Gps.value['latitude']
                lon = Gps.value['longitude']
                Upload.setGPS(latitude=lat,longitude=lon)
                print("[testUpload] Set GPS:",{'latitude':lat,'longitude':lon})
            
            if Dht11.ready == True:
                hum = Dht11.humidity
                tem = Dht11.temperature
                Upload.setDHT(temperature=tem,humidity=hum)
                print("[testUpload] Set DHT:",{'temperature':tem,'humidity':hum})
        else:
            Upload.setGPS(latitude=24.145,longitude=120.671)
            Upload.setDHT(temperature=25,humidity=42)
            print("[testUpload] Set Fake Data")

        time.sleep(1/freq)
except BaseException as e:
    print("[TestSensor] Capture Exception while runnung!")
    print(type(e), str(e))

finally:
    for thread in threads:
        thread[1].stop()
    for thread in threads:
        thread[1].join()         
        
