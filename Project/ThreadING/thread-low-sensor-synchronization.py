#!/usr/bin/python3

import _thread
import time

distance = 0

def distanceSensor():
    global distance
    count = 0
    print("DistanceSensor thread start.\n")
    while(count < 40):
        if (count % 6 == 0):
            time.sleep(0.02)
        if (count == 37):
            _thread.exit()
        count = count +1
        distance = count % 10
        print("[Distance] %5d . Set distance %d\n"%(count,count % 10))
        time.sleep(0.01)
    print("Thread End")
    


distanceThread = _thread.start_new_thread(distanceSensor,())
#distanceThread.start()
count = 0

try:
    while(count < 60):
        count = count +1
        print("[Main    ] %5d . Get distance %d\n"%(count,distance))
        time.sleep(0.01)
finally:
    _thread.exit()
    #distanceThread.exit()
