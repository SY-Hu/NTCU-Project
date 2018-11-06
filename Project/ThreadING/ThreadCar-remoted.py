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
updateFreq        = 1000


########## Import File ##########
import RPi.GPIO as GPIO
import ThreadCarDriver
import ThreadCommunication
import threading
import time
import datetime 
import queue


########## Execution Code ##########
threadList = []
myID = "SC-01"
myName = "SlaveCar1"

##### Establish threads to sensoring
car = ThreadCarDriver.CarDriver()
threadList.append((car,"Car"))
thread_Send = ThreadCommunication.SendThread()
threadList.append((thread_Send,"Send"))
thread_Receive = ThreadCommunication.ReceiveThread()
threadList.append((thread_Receive,"Receive"))
import get_IP
myIP = get_IP.getIP()

knownDevice = {'masterCar':{},'slaveCar':{},'side':{}}
thread_Send.send({'type':'discover','context':{'id':myID,'name':myName,'type':'slaveCar'}},get_IP.getBroadcastIP(),repeat=True)

##### Loop
try:
    print("[CarSlave] Car slave start run loop.")
    while True:
        #### Get Remote command ####
        for i in range(0,2):
            ThreadCommunication.qlock.acquire()
            if debug:
                print("[Debug] Car get lock.")
            if not ThreadCommunication.receivedQueue.empty():
                data = ThreadCommunication.receivedQueue.get()
                ThreadCommunication.qlock.release()
                pack = data['receive']
                
                ##### Discover type
                if pack['type'] == 'discover':
                    deviceType = pack['context']['type']
                    if not data['ip'] in knownDevice[deviceType]:
                        #if debug:
                        print("[Debug] Get New Device : %s %s"%(deviceType,pack['context']['name'])) 
                        if deviceType == 'side':
                            knownDevice['side'][data['ip']] = {'id':pack['context']['id'],'name':pack['context']['name'],'control':pack['context']['control']}
                        if deviceType == 'masterCar':
                            knownDevice['slaveCar'][data['ip']] = {'id':pack['context']['id'],'name':pack['context']['name']}
                    else: # Has recorded before
                        pass
                        
                ##### Car Command type
                elif pack['type'] == 'carCommand':
                    car.assign(pack['context']['command'],pack['context']['time'])
                    car.status()
                    
                ##### Other messeage type
                else: 
                    pass
                    
            else:
                try:
                    ThreadCommunication.qlock.release()
                except:
                    print("[Error] Unlock not locked lock in small.")
                    pass
                break
            
        sleep(1/updateFreq)

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
