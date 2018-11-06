#! /usr/bin/python

#########################################
# NTCU Computer Science 
# Project 107 - 08 
# Program : Auto TraceLine Car
#            with Wifi Sender
#########################################

print("NTCU Computer Science Project 107-08")
print("Program : Roadside Device Program")
print("Program Side start. ")

########## Basic Setup ##########
# Import files
import RPi.GPIO as GPIO
import ThreadCommunication
import threading
import queue
import get_IP
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

freq = 2000

# Define Support Device
LED = {"roadlight1":19}
for lightName,pin in LED.items():
    GPIO.setup(pin,GPIO.OUT)

# ##building for auto config support device
ledList = [ key for key,value in LED.items()]
controlable = {"led":ledList}

# Define variable
broadcastIP = get_IP.getBroadcastIP()
threads = []
myID = 'RS-01'
myIP = get_IP.getIP()
myName = 'roadlight'
knownDevice = {'masterCar':{},'slaveCar':{},'side':{}}
 
# Start Thread
sendThread = ThreadCommunication.SendThread(repeatFreq = 0.2)
threads.append(sendThread)
receiveThread = ThreadCommunication.ReceiveThread() 
threads.append(receiveThread)
for thread in threads:
    thread.start()
    
########## Main ##########
# Broadcast myself
broadcastData = {'type':'discover','context':{'id':myID,'name':myName,'type':'side','control':{'led':['roadlight1']}}}
sendThread.send(broadcastData,broadcastIP,repeat=True)

# Check whether has new data received
try:
    print("[ Side ] Program Start.")
    while True:
        ThreadCommunication.qlock.acquire()
        if not ThreadCommunication.receivedQueue.empty():
            data = ThreadCommunication.receivedQueue.get()
            print("[Debeg ] Receive:",data)
            ThreadCommunication.qlock.release()
        
            pack = data['receive']
            
            ##### Side Command type
            if pack['type'] == 'sideCommand':
                for key,value in pack['context'].items():
                    if key == 'led':
                        for lightName,action in value.items():
                            if action == 'on':
                                GPIO.output(LED[lightName], GPIO.HIGH)
                                print("[ Side ] LED - ",LED[lightName]," on.")
                            elif action == 'off':
                                GPIO.output(LED[lightName], GPIO.LOW)
                                print("[ Side ] LED - ",LED[lightName]," off.")
                            else: # Unknown action
                                pass

            ##### Discover type
            elif pack['type'] == 'discover':
                deviceType = pack['context']['type']
                if not data['ip'] in knownDevice[deviceType]:
                    knownDevice[deviceType][data['ip']] = {'id':pack['context']['id'],'name':pack['context']['name']}
                else: # Has recorded before
                    pass
        else:
            try:
                ThreadCommunication.qlock.release()
            except:
                print("[Error] Unlock not locked lock in Small.")
            print("[Debeg ] Receive queue empty.")
        
        time.sleep(1/freq)
except BaseException as e:
    print("[ Side ] Capture Exception while looping!")
    print(type(e), str(e))
finally:
    ########## End ##########
    print("[ Side ] Program exiting.")
    GPIO.cleanup()
    try:
        ThreadCommunication.qlock.release()
    except:
        print("[Error] Unlock not locked lock in Big.")
    for thread in threads:
        thread.stop()
        thread.join()
    print("[ Side ] Program exit.")
