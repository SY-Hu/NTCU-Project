#! /usr/bin/python

#########################################
# NTCU Computer Science 
# Project 107 - 08 
# Program : Car Communication Thread
#
#########################################

print("NTCU Computer Science Project 107-08")
print("Program : Car Communication Thread")
print("Program start. ")

########## import ##########
import queue
import json
import time
import socket
import datetime
import threading

########## Upload Data ##########
class UploadData(threading.Thread):
    def __init__(self,freq=1,toSensor=True,toGPS=True):
        import MySQLdb
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.freq = freq
        self.toSensor = toSensor
        self.toGPS = toGPS
        self.latitude = None
        self.longitude = None
        self.temperature = None
        self.humidity = None
        try:
            self.db = MySQLdb.connect(host="car.leafu.one", port=3307 , user='nopass', passwd='bH5cpZ8VOg4wCPX!', db="test")
            self.cur = self.db.cursor()
            print("[UploadData] DataBase Connect.")
        except BaseException as e:
            print("[UploadData] Capture Exception! Database connect failed!")
            print(type(e), str(e))
    
    def run(self):
        while(not self._stop_event.is_set()):
            latitude = self.latitude
            longitude = self.longitude
            if not self.latitude == None and not self.longitude == None:
                # Execute insert gps sql
                if self.toGPS:
                    query = ("INSERT INTO gps (gpslat,gpslng,username) VALUES (%s,%s,%s)")
                    data = (latitude, longitude, 'car')
                    self.cur.execute(query, data)
                    self.db.commit()
                if not self.temperature == None and not self.humidity == None:
                    # Execute insert sensor sql
                    if self.toSensor:
                        querye = ("INSERT INTO sensor (gpslat, gpslng, temperature, humidity, username) VALUES (%s,%s,%s,%s,%s)")
                        sen = (latitude, longitude, self.temperature, self.humidity, 'car')
                        self.cur.execute(querye, sen)
                        self.db.commit()
                print("[UploadData] Data Uploaded.") 
            time.sleep(1/self.freq)
    
    def setDHT(self,temperature=None,humidity=None):
        self.temperature = temperature
        self.humidity = humidity
        
    def setGPS(self,latitude=None,longitude=None):
        self.latitude = latitude
        self.longitude = longitude
        
    def stop(self):
        self._stop_event.set()
    
    def __del__(self):
        print("[Updating] Thread end.")

        
########## Sending Data ##########        
class SendThread(threading.Thread):
    def __init__(self,repeatFreq=1):
        import time
        import socket
        import get_IP
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.UDP_IP = get_IP.getBroadcastIP()
        self.command = ""
        self.repeat = []
        self.repeatFreq = repeatFreq
        print("[Sending] SendThread thread start.")
    
    def run(self):
        while(not self._stop_event.is_set()):
            print("[Sending] Regular Send.")
            for toSend in self.repeat:
                toSend['data']['no'] = toSend['data']['no'] + 1
                self.sock.sendto(json.dumps(toSend['data'],separators=(',',':')).encode(),(toSend['ip'],toSend['port']))

            time.sleep(1/self.repeatFreq)    
        
    def send(self,command,targetIP,targetPort=5005,repeat=False): #change to json later
        command['no'] = 1 
        print("[Sending] Sending.")        
        self.sock.sendto(json.dumps(command,separators=(',',':')).encode(),(targetIP,targetPort))
        if repeat == True:
            for item in self.repeat:
                if item['ip'] == targetIP and item['port'] == targetPort:
                    item['data'] = command
                    break
            else:
                self.repeat.append({'data':command,'ip':targetIP,'port':targetPort})
        
    def noSend(self,command):
        for item in self.repeat:
            if command in item[data]:
                del item
                return True
        else:
            return False
    
    def stop(self):
        self._stop_event.set()
    
    def __del__(self):
        print("[Sending] Thread end.")
    
    
########## Receiving Data ##########
qlock = threading.Lock()
#nearDevice = {}
receivedQueue = queue.Queue(10)        
class ReceiveThread(threading.Thread):
    def __init__(self,port=5005):
        import socket
        import get_IP
        import queue
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.receiveNoRecord = {}
        self.port = port
        #self.lock = lock
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sock.bind(('', port))
        self.myIP = get_IP.getIP()
        global nearDevice
        print("[Receiving] Receiving thread start.")
        
    def run(self):
        global queue
        global qlock
        while(not self._stop_event.is_set()):
            global receivedQueue
            receive = self.sock.recvfrom(4096)
            data = json.loads(receive[0].decode())
            #print("[Debug ] Receive: ",data)
            receiveIP = receive[1][0]
            if receiveIP == self.myIP:
                pass
            elif receiveIP in self.receiveNoRecord: # If received packet's ip in no. record.
                if self.receiveNoRecord[receiveIP]['no'] < data['no']: # If received no. is bigger than recorded ,else drop.
                    del data['no']
                    if self.receiveNoRecord[receiveIP]['data'] != data: # If received data is different from before ,pass to main car ,else drop.
                        qlock.acquire()
                        #print("[Debug ] Type of q:",type(receivedQueue))
                        receivedQueue.put({"receive":data,"ip":receiveIP})
                        qlock.release()
                        
            else: # Received IP isn't seen before ,add to record.
                self.receiveNoRecord[receiveIP] = {'no':1,'data':data}

    def stop(self):
        self._stop_event.set()

    def __del__(self):
        qlock.release()
        print("[Receiving] Thread end.")        

