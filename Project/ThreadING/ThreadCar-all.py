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
backDistance      =  10       # Set 0 to Disable , Max to maxDistance 
updateFreq        = 2000
enableTraceLine   = True
enableDistance    = True
enableGPS         = True
enableDHT11       = True
enableLight       = True
enableConnection  = True
enableSlave       = True
enableSide        = True
enableUploadData  = True

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
class MainCar(threading.Thread):
    def __init__(self,freq=1000,maxDist=10,backDist=None,Name="MasterCar1",ID="MSC-01"):
        print("[CarMain] Car Main program start.")
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.maxDist = maxDist
        self.freq = freq
        self.threadList = []
        self.myID = ID
        self.myName = Name
        if backDist != None:     
            if backDist > maxDist:
                self.backDist = maxDist
            elif backDist < 0 or backDist == None:
                self.backDist = 0
            else:
                self.backDist = backDist
        else:
            self.backDist = 0
    
    def run(self):
        ##### Establish threads to sensoring
        self.car = ThreadCarDriver.CarDriver()
        self.threadList.append((self.car,"Car"))
        if enableTraceLine:
            self.thread_Linesensor_L = ThreadSensor.LineSensor(traceline_L)
            self.thread_Linesensor_R = ThreadSensor.LineSensor(traceline_R)
            self.threadList.append((self.thread_Linesensor_L,"Line_L"))
            self.threadList.append((self.thread_Linesensor_R,"Line_R"))
        if enableDistance:
            self.thread_Distance = ThreadSensor.DistanceSensor(echo=distance_echo,trig=distance_trigger,led=distance_led,ir=distance_ir,maxDis=self.maxDist)
            self.threadList.append((self.thread_Distance,"Distance"))
        if enableGPS:
            self.thread_Gps = ThreadSensor.GPSMeter()
            self.threadList.append((self.thread_Gps,"GPS"))
        if enableDHT11:
            self.thread_Dht11 = ThreadSensor.DHT11Sensor(pin=dht11_pin)
            self.threadList.append((self.thread_Dht11,"DHT11"))
        if enableLight:
            self.thread_Light = ThreadSensor.LightSensor()
            self.threadList.append((self.thread_Light,"Light"))
        if enableConnection:
            self.qlock = threading.Lock()
            self.thread_Send = ThreadCommunication.SendThread()
            self.threadList.append((self.thread_Send,"Send"))
            self.thread_Receive = ThreadCommunication.ReceiveThread()
            self.threadList.append((self.thread_Receive,"Receive"))
            import get_IP
            self.myIP = get_IP.getIP()

            self.knownDevice = {'masterCar':{},'slaveCar':{},'side':{}}
            #self.controlable = {}
            self.thread_Send.send({'type':'discover','context':{'id':self.myID,'name':self.myName,'type':'masterCar'}},get_IP.getBroadcastIP(),repeat=True)
        global enableUploadData
        if enableUploadData:
            if enableGPS:
                if enableDHT11:
                    self.thread_Upload = ThreadCommunication.UploadData()
                else:
                    self.thread_Upload = ThreadCommunication.UploadData(toSensor = False)
                self.threadList.append((self.thread_Upload,"Upload"))
            else:
                print("[CarMain] To upload data need GPS enabled.")
                print("[CarMain] Disable Upload function.")
                enableUploadData = False

        print("[Debug] Ready to start threads.")
        for thread in self.threadList:
            if debug:
                print("[Debug] Starting Thread %s"%(thread[1]))
            thread[0].start()  
            
        ##### Loop 
        while True:
            print("[CarMain] Car start run loop.")
            while(not self._stop_event.is_set()):
                ########## Loop Car
                if debug:
                    print("[Debug] Car main.")
                ##### Get sensor data
                if enableTraceLine:
                    lineL = self.thread_Linesensor_L.value
                    lineR = self.thread_Linesensor_R.value
                if enableDistance:    
                    dist = self.thread_Distance.value
                ##### Car main execution               
                persistTime = 0
                if enableDistance and enableDistance:
                    if dist < self.maxDist :
                        if dist < self.backDist:
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
                    if dist < self.maxDist :
                        if dist < self.backDist:
                            command = "Back"
                            persistTime = 1
                        else:
                            command = "Stop"
                
                else:
                    command = "Go"
                    
                if debug:
                    pass
                print("[Debug] Car assign command to car.")   
                self.car.assign(command,persistTime)
                self.car.status()
 
                ########## Loop Sensor
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
                                if not data['ip'] in self.knownDevice[deviceType]:
                                    #if debug:
                                    print("[Debug] Get New Device : %s %s"%(deviceType,pack['context']['name'])) 
                                    if deviceType == 'side':
                                        self.knownDevice['side'][data['ip']] = {'id':pack['context']['id'],'name':pack['context']['name'],'control':pack['context']['control']}
                                    if deviceType == 'slaveCar':
                                        self.knownDevice['slaveCar'][data['ip']] = {'id':pack['context']['id'],'name':pack['context']['name']}
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
                        for deviceIP,deviceDetail in self.knownDevice['slaveCar'].items():
                            self.thread_Send.send({'type':'carCommand','context':{'command':command,'time':persistTime}},deviceIP,repeat=True)
                            
                    if enableSide:
                        if enableLight: 
                            if self.thread_Light.value == 'light':
                                lightCommand = "off"
                            else:
                                lightCommand = "on"
                                
                            for deviceIP,deviceDetail in self.knownDevice['side'].items():
                                if enableLight:
                                    sendLight = {}
                                    for led in deviceDetail['control']['led']:
                                        sendLight.update({led:lightCommand})
                                        
                                    self.thread_Send.send({'type':'sideCommand','context':{'led':sendLight}},deviceIP,repeat=True)
                                
                if enableUploadData:
                    if not self.thread_Gps.value['latitude'] == 0 and not self.thread_Gps.value['longitude'] == 0:
                        lat = self.thread_Gps.value['latitude']
                        lon = self.thread_Gps.value['longitude']
                        self.thread_Upload.setGPS(latitude=lat,longitude=lon)   
                    
                    if enableDHT11:
                        if self.thread_Dht11.ready == True:
                            hum = self.thread_Dht11.humidity
                            tem = self.thread_Dht11.temperature
                            self.thread_Upload.setDHT(temperature=tem,humidity=hum)
         
        #except BaseException as e:
        #    print("[CarMain] Capture Exception while looping!")
        #    print(type(e), str(e))
        
        #finally:
        #    try:
        #        ThreadCommunication.qlock.release()
        #    except:
        #        print("[Error] Unlock not locked lock in Big.")
        #
        else:    
            print("[CarMain] Exiting")
            for thread in self.threadList:
                thread[0].stop()
            time.sleep(1)
            for thread in self.threadList:
                print("[CarMain] Is thread ",thread[1],"alive? ",thread[0].is_alive())
            
            
    def stop(self):
        self._stop_event.set() 

    def __del__(self):
        pass
        


try:
    mainCar = MainCar()
    mainCar.start()
    mainCar.join()
except:
    mainCar.stop()
finally:
    mainCar.join()
    GPIO.cleanup()


