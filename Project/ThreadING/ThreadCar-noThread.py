#! /usr/bin/python

#########################################
# NTCU Computer Science 
# Project 107 - 08 
# Program : Auto TraceLine Car
#            with Wifi Sender
#########################################

print("NTCU Computer Science Project 107-08")
print("Program : Auto TraceLine Car with Wifi Sender")
print("Program AutoCar start. ")

########## Control ##########
# Setup Control Variable
maxDistance       =  12
maxTemperture     =  40
backDistance      =  0       # Set 0 to Disable , Max to maxDistance 
updateFreq        = 500
enableTraceLine   = True
enableDistance    = True
enableGPS         = True
enableDHT11       = True
enableLight       = True
enableConnection  = True
enableSlave       = True
enableSide        = True
enableUploadData  = True
enableSMS         = True
debug             = False

# Setup GPIO Pin
distance_trigger  =  17
distance_echo     =  16
distance_led      =  18
distance_ir       =  13
traceline_L       =   4
traceline_R       =   6
dht11_pin         =  12

########## Import File ##########
import RPi.GPIO as GPIO
import ThreadCarDriver
import ThreadCommunication
import ThreadSensor
import threading
import time
import datetime 
import queue
from time import sleep

########## Execution Code ##########
maxDist = maxDistance
backDist = backDistance
freq = updateFreq
threadList = []
errorList = []
myID = "MSC-01"
myName = "MasterCar1"

if backDist != None:     
    if backDist > maxDist:
        backDist = maxDist
    elif backDist < 0 or backDist == None:
        backDist = 0
    else:
        backDist = backDist
else:
    backDist = 0
    
##### Establish threads to sensoring
car = ThreadCarDriver.CarDriver(inp1=22,inp2=27,inp3=24,inp4=23,goSp=48,turnSp=50)
threadList.append((car,"Car"))
if enableTraceLine:
    thread_Linesensor_L = ThreadSensor.LineSensor(traceline_L)
    thread_Linesensor_R = ThreadSensor.LineSensor(traceline_R)
    threadList.append((thread_Linesensor_L,"Line_L"))
    threadList.append((thread_Linesensor_R,"Line_R"))
if enableDistance:
    thread_Distance = ThreadSensor.DistanceSensor(echo=distance_echo,trig=distance_trigger,led=distance_led,ir=distance_ir,maxDis=maxDist)
    threadList.append((thread_Distance,"Distance"))
if enableGPS:
    thread_Gps = ThreadSensor.GPSMeter()
    threadList.append((thread_Gps,"GPS"))
if enableDHT11:
    thread_Dht11 = ThreadSensor.DHT11Sensor(pin=dht11_pin)
    threadList.append((thread_Dht11,"DHT11"))
if enableLight:
    thread_Light = ThreadSensor.LightSensor(upper = 80,lower = 79)
    threadList.append((thread_Light,"Light"))
    sendLight = {}
if enableConnection:
    thread_Send = ThreadCommunication.SendThread()
    threadList.append((thread_Send,"Send"))
    thread_Receive = ThreadCommunication.ReceiveThread()
    threadList.append((thread_Receive,"Receive"))
    import get_IP
    myIP = get_IP.getIP()

    knownDevice = {'masterCar':{},'slaveCar':{},'side':{}}
    #controlable = {}
    thread_Send.send({'type':'discover','context':{'id':myID,'name':myName,'type':'masterCar'}},get_IP.getBroadcastIP(),repeat=True)
if enableSMS:
    import twilio.rest
    account_sid = "AC17b9c6052ec5171f65eb484be72df9de"
    auth_token = "eef3987b76d7ca85edda83d5a8e8a756"
    client = twilio.rest.Client(account_sid, auth_token)

if enableUploadData:
    if enableGPS:
        if enableDHT11:
            thread_Upload = ThreadCommunication.UploadData()
        else:
            thread_Upload = ThreadCommunication.UploadData(toSensor = False)
        threadList.append((thread_Upload,"Upload"))
    else:
        print("[CarMain] To upload data need GPS enabled.")
        print("[CarMain] Disable Upload function.")
        enableUploadData = False

print("[Debug] Ready to start threads.")
for thread in threadList:
    if debug:
        print("[Debug] Starting Thread %s"%(thread[1]))
    thread[0].start()  
    
##### Loop 
try:
    print("[CarMain] Car start run loop.")
    while True:
        ########## Loop Car
        if debug:
            print("[Debug] Car main.")
        ##### Get sensor data
        if enableTraceLine:
            lineL = thread_Linesensor_L.value
            lineR = thread_Linesensor_R.value
        if enableDistance:    
            dist = thread_Distance.value
        ##### Car main execution               
        persistTime = 0
        if enableDistance and enableDistance:
            if dist < maxDist :
                if dist < backDist:
                    command = "Back"
                    persistTime = 1
                else:
                    command = "Stop"
            else: 
                if lineL == 'white' and lineR == 'white':
                    command = "Go"
                elif lineL == 'black' and lineR == 'white':
                    command = "Left"
                elif lineL == 'white' and lineR == 'black':
                    command = "Right"
                else:
                    command = "Go"
        
        elif not enableDistance and enableDistance:
            if lineL == 'white' and lineR == 'white':
                command = "Go"
            elif lineL == 'black' and lineR == 'white':
                command = "Left"
            elif lineL == 'white' and lineR == 'black':
                command = "Right"
            else:
                command = "Go"

        elif enableDistance and not enableDistance:
            if dist < maxDist :
                if dist < backDist:
                    command = "Back"
                    persistTime = 1
                else:
                    command = "Stop"
        
        else:
            command = "Go"
            
        if debug:
            print("[Debug] Car assign command to car.")   
        car.assign(command,persistTime)
        car.status()

        ########## Loop Sensor
        if debug:
            print("[Debug] Car sensor.")
        if enableConnection:
            if debug:
                print("[Debug] Car in connection.")
            for i in range(0,2):
                ThreadCommunication.qlock.acquire()
                if debug:
                    print("[Debug] Car get lock.")
                if not ThreadCommunication.receivedQueue.empty():
                    data = ThreadCommunication.receivedQueue.get()
                    ThreadCommunication.qlock.release()
                    pack = data['receive']
                    if pack['type'] == 'discover':
                        deviceType = pack['context']['type']
                        if not data['ip'] in knownDevice[deviceType]:
                            #if debug:
                            print("[Debug] Get New Device : %s %s"%(deviceType,pack['context']['name'])) 
                            if deviceType == 'side':
                                knownDevice['side'][data['ip']] = {'id':pack['context']['id'],'name':pack['context']['name'],'control':pack['context']['control']}
                            if deviceType == 'slaveCar':
                                knownDevice['slaveCar'][data['ip']] = {'id':pack['context']['id'],'name':pack['context']['name']}
                        else: # Has recorded before
                            pass
                    else: # Other messeage not discover type
                        pass
                else:
                    try:
                        ThreadCommunication.qlock.release()
                    except:
                        print("[Error] Unlock not locked lock in small.")
                        pass
                    break
            
            if enableSlave:
                for deviceIP,deviceDetail in knownDevice['slaveCar'].items():
                    thread_Send.send({'type':'carCommand','context':{'command':command,'time':persistTime}},deviceIP,repeat=True)
                    
            if enableSide:
                if enableLight: 
                    if thread_Light.value == 'light':
                        lightCommand = "off"
                    else:
                        lightCommand = "on"
                    sendLight = {}    
                    for deviceIP,deviceDetail in knownDevice['side'].items():
                        if enableLight:
                            
                            for led in deviceDetail['control']['led']:
                                sendLight.update({led:lightCommand})
                                
                            thread_Send.send({'type':'sideCommand','context':{'led':sendLight}},deviceIP,repeat=True)
                            if debug:
                                pass
                            print("[Debug] Send SideCommand = ",{'type':'sideCommand','context':{'led':sendLight}})
                            
        if enableUploadData:
            if not thread_Gps.value['latitude'] == 0 and not thread_Gps.value['longitude'] == 0:
                lat = thread_Gps.value['latitude']
                lon = thread_Gps.value['longitude']
                thread_Upload.setGPS(latitude=lat,longitude=lon)   
            
            if enableDHT11:
                if thread_Dht11.ready == True:
                    hum = thread_Dht11.humidity
                    tem = thread_Dht11.temperature
                    thread_Upload.setDHT(temperature=tem,humidity=hum)
        
        if enableSMS:
            if enableDHT11:
                if thread_Dht11.ready == True:
                    if thread_Dht11.temperature > maxTemperture:
                        message = client.messages.create(
                            "+8860978912385",
                            body="[MasterCar] Warning! OverHeat!",
                            from_="+14437072667"
                        )
                        
                        message.sid
                        enableSMS = False
                        
        for thread in threadList:
            if thread[0].is_alive() == False:
                if not thread[1] in errorList:
                    errorList.append(thread[1])
                    thread[0].start()
                else:
                    print("[Error] Thread %s stopped,and restart failed."%(thread[1]))
                    raise Exception("[Error] Thread %s stopped,and restart failed."%(thread[1]))
            else:
                if thread[1] in errorList:
                    errorList.remove(thread[1])
        
        time.sleep(1/updateFreq)
 
except BaseException as e:
    print("[CarMain] Capture Exception while looping!")
    print(type(e), str(e))

finally:
    try:
        ThreadCommunication.qlock.release()
    except:
        print("[Error] Unlock not locked lock in Big.")
    
    print("[CarMain] Exiting")
    for thread in threadList:
        thread[0].stop()
    time.sleep(1)
    for thread in threadList:
        print("[CarMain] Is thread ",thread[1],"alive? ",thread[0].is_alive())
            
    GPIO.cleanup()


