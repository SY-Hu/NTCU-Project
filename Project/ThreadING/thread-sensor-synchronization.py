#!/usr/bin/python3

import threading
import time

dis = -1
stri = "ASC"

class distanceSensor(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.distance = 0
        self.name = name
        self.__str = "A"
        
    def run(self):
        
        #global distance
        count = 0
        print("DistanceSensor thread start.\n")
        while(count < 40 and not self._stop_event.is_set()):
            if (count % 6 == 0):
                time.sleep(0.02)
            count = count +1
            self.distance = count % 10
            print("[Distance] %s %5d . %s Set distance %d %s\n"%(self.name,count,self.__str,self.distance,stri))
            time.sleep(0.01)
        print("Thread End")
        
    def getDistance(self):
        return self.distance
        
    def stop(self):
        self._stop_event.set()

distanceThread = distanceSensor("alpha")
distanceThread2 = distanceSensor("beta")
distanceThread.start()
distanceThread2.start()
count = 0

try:
    while(count < 30):
        count = count +1
        dis1 = distanceThread.distance
        dis2 = distanceThread2.distance
        distanceThread._distanceSensor__str = "Main"
        print("[Main    ] %5d . Get distance dis1=%d dis2=%d\n"%(count,dis1,dis2))
        time.sleep(0.01)
finally:
    distanceThread.stop()
    print("Main End")
