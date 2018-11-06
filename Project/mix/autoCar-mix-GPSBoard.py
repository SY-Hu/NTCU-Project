#! /usr/bin/python
import RPi.GPIO as gpio
import os
import sys
import time
import datetime
import socket
import MySQLdb
import dht11
import logging
from time import sleep
from gps3 import gps3

print("AutoCar with Sensor - Wifi Sender.")
print("Program start. ")

########## Control ##########
# Setup Global Variable
maxDistance = 10
enableTraceLine = True
isStopped = True
turnPercent = 50
enableDistance = True
sensing = True
querytosql = True

########## Connection ##########
# Setup Wifi Connection (Client)
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
UDP_IP = "192.168.43.255"
UDP_PORT = 5005

# Setup MySQL connection
if querytosql:
    db = MySQLdb.connect(host="car.leafu.one", port=3307 , user='nopass', passwd='bH5cpZ8VOg4wCPX!', db="test")
    cur = db.cursor()
    print("DataBase Connect.")

########## Sensors ##########
# Setup GPIO
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
data=""

# Setup LED
ledLeft = 7
ledRight = 12
ledDisLeft = 24
ledDisRight = 25
gpio.setup(ledRight, gpio.OUT)
gpio.setup(ledLeft, gpio.OUT)
gpio.setup(ledDisRight, gpio.OUT)
gpio.setup(ledDisLeft, gpio.OUT)

# Setup DistanceSensor
echo1 = 19
echo2 = 17
trigger1 = 20
trigger2 = 18
gpio.setup(trigger1, gpio.OUT)
gpio.setup(trigger2, gpio.OUT)
gpio.setup(echo1, gpio.IN)
gpio.setup(echo2, gpio.IN)
leftturn = True


def distanceCalc(pin,tri):
    # set Trigger to HIGH
    gpio.output(tri, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    gpio.output(tri, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while gpio.input(pin) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while gpio.input(pin) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    if TimeElapsed <= 0:
        TimeElapsed = 1
        print(pin ,' time too small.')
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    
    if distance > 500:
        distance = 500
    
    if enableDistance:
        return distance
    else:
        return 100
        
distanceR = distanceCalc(echo1, trigger1)
distanceL = distanceCalc(echo2, trigger2)       

# Setup LineSensor
readlineL = 21
readlineM = 22
readlineR = 23

gpio.setup(readlineL,gpio.IN)
gpio.setup(readlineM,gpio.IN)
gpio.setup(readlineR,gpio.IN)

# Setup DHT11
th = dht11.DHT11( pin = 16 )

# Setup GPS
gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()

########## Car ##########
# Define input pin
ain1 = 15 
ain2 = 2
ain3 = 3
ain4 = 27

# Set default duty cycle
motor = [0,0,0,0] # L1,L2 , R1,R2
 
gpio.setup(ain1, gpio.OUT)
gpio.setup(ain2, gpio.OUT)
gpio.setup(ain3, gpio.OUT)
gpio.setup(ain4, gpio.OUT)

# Set to gpio 
m1 = gpio.PWM(ain1, 30)
m2 = gpio.PWM(ain2, 30)
m3 = gpio.PWM(ain3, 30)
m4 = gpio.PWM(ain4, 30)

m1.start(0)
m2.start(0)
m3.start(0)
m4.start(0)

# Define function to command the car
def start():
    motor[0:3] = [55,0,55,0]
    data="START"
    exe()
    isStopped = False
    sleep(0.001)

def go():
    if isStopped:
        print("Command: START     ", end='')
        start()
    motor[0:3] = [40,0,40,0]
    data="GO"
    gpio.output(ledLeft,gpio.LOW)
    gpio.output(ledRight,gpio.LOW)
    exe()

def stop():
    motor[0:3] = [0,0,0,0]
    data="STOP"
    gpio.output(ledLeft,gpio.HIGH)
    gpio.output(ledRight,gpio.HIGH)
    isStopped = True
    exe()

def back():
    motor[0:3] = [0,50,0,50]
    data="BACK"
    gpio.output(ledLeft,gpio.LOW)
    gpio.output(ledRight,gpio.LOW)
    exe()

def turnRight():
    motor[0:3] = [50,0,0,50]
    data="TURN RIGHT"
    gpio.output(ledLeft,gpio.LOW)
    gpio.output(ledRight,gpio.HIGH)
    exe()

def right():
    #motor[0]+= 3
    #motor[2]-= 3
    if isStopped:
        print("Command: START     ", end='')
        start()
    motor[0:3] = [turnPercent,0,0,0]
    data="RIGHT"
    gpio.output(ledLeft,gpio.LOW)
    gpio.output(ledRight,gpio.HIGH)
    exe()

def turnLeft():
    motor[0:3] = [0,50,50,0]
    data="TRUN LEFT"
    gpio.output(ledLeft,gpio.HIGH)
    gpio.output(ledRight,gpio.LOW)
    exe()

def left():
    #motor[0]-= 3
    #motor[2]+= 3
    if isStopped:
        print("Command: START     ", end='')
        start()
    motor[0:3] = [0,0,turnPercent,0]
    data="LEFT"
    gpio.output(ledLeft,gpio.HIGH)
    gpio.output(ledRight,gpio.LOW)
    exe()

def slowGo():
    if isStopped:
        print("Command: START     ", end='')
        start()
    motor[0:3] = [40,0,40,0]
    data="SLOW GO"
    gpio.output(ledLeft,gpio.LOW)
    gpio.output(ledRight,gpio.LOW)
    exe()

def exe():
    
    for i in range(4):
        if motor[i] > 100:
            motor[i] = 100
            print("motor [",i,"] is too large")
        elif motor[i] < 0:
            motor[i] = 0
            print("motor [",i,"] is too small")


    print("motor:{0:d},{1:d},{2:d},{3:d}".format(motor[0],motor[1],motor[2],motor[3]))
    #set to motor
    m1.ChangeDutyCycle(motor[0])
    m2.ChangeDutyCycle(motor[1])
    m3.ChangeDutyCycle(motor[2])
    m4.ChangeDutyCycle(motor[3])
    
    sock.sendto(data.encode(), (UDP_IP, UDP_PORT))


print("Setup Finished")

########## Execution Code ##########
try:
    while True:
        readL = gpio.input(readlineL)
        readM = gpio.input(readlineM)
        readR = gpio.input(readlineR)
        if leftturn:
            distanceR = distanceCalc(echo1, trigger1)
            leftturn = False
        else:    
            distanceL = distanceCalc(echo2, trigger2)
            leftturn = True
        gpio.output(ledDisRight, gpio.LOW)
        gpio.output(ledDisLeft, gpio.LOW)
        #if sensing:
        #    HumiTemp = th.read()
        
        #### Car ####
        #UI
        print('DisL  LineL  LineM  LineR  DisR  ')
        print('{0:3.2f}  {1:d}      {2:d}     {3:d}    {4:3.2f}'.format(distanceL,readL,readM,readR,distanceR))


        if readL == 0 and readM == 1 and readR == 0 and distanceL > maxDistance and distanceR > maxDistance:
            print("Command: GO        ", end='')
            go()
        elif readL == 1 and readR == 0 and distanceL > maxDistance and distanceR > maxDistance and enableTraceLine:
            # Go Left
            print("Command: LEFT      ", end='')
            left()
            sleep(0.3)
        elif readL == 0 and readR == 1 and distanceL > maxDistance and distanceR > maxDistance and enableTraceLine:
            # Go Right
            print("Command: RIGHT     ", end='')
            right()
            sleep(0.3)
        elif readL == 0 and readM == 0 and readR == 0 and distanceL > maxDistance and distanceR > maxDistance:
            # All No Line
            #print("Command: STOP (!)  ", end='')
            #stop()
            print("Command: SKIP")
        elif readL == 1 and readM == 1 and readR == 1 and distanceL > maxDistance and distanceR > maxDistance:
            # All On Line
            print("Command: GO (!)     ", end='')
            go()
        elif distanceL < maxDistance or distanceR < maxDistance:
            # Led Control
            if distanceL < maxDistance:
                gpio.output(ledDisLeft,gpio.HIGH)
            if distanceR < maxDistance:
                gpio.output(ledDisRight,gpio.HIGH)

            print("Command: STOP      ", end='')
            stop()
            if distanceL < 8 or distanceR < 8:
                print("Command: BACK      ", end='')
                back()
                sleep(0.2)
                print("Command: STOP      ", end='')
                stop()
            sleep(0.8)
            if distanceL < maxDistance:
                print("Command: RUEN RIGHT", end='')
                turnRight()
            elif distanceR < maxDistance:
            #    print("Command: TURN LEFT ", end='')
            #    turnLeft()
                print("Command: TURN RIGHT ", end='')
                turnRight()
            else:
                print("Command: RUEN RIGHT", end='')
                turnRight()
            sleep(0.2)
        else:
            print("Command: Slow Go   ", end='')
            slowGo()
        
        # UI status
        if readL == 0 and readM == 0 and readR == 0:
            print("Car can't find line.")
        elif readL == 1 and readM == 1 and readR == 1:
            print("Car is all on line.")
        else:
            print(" ")


        print('==========================')
        
        #### Sensor ####
        if sensing:

            
            # Humidity Temperature
            htread = th.read()
            
            if htread.is_valid():
                print("Temperature: %d C" % htread.temperature)
                print("Humidity: %d %%" % htread.humidity)  
            else:
                print("Temperature: n/a")
                print("Humidity: n/a")

            # GPS
            for new_data in gps_socket:
                if new_data:
                    data_stream.unpack(new_data)
                    print('Altitude = ', data_stream.TPV['alt'])
                    print('Latitude = ', data_stream.TPV['lat'])
                    print('Longitude = ', data_stream.TPV['lon'])
                else:
                    print('Altitude = n/a')
                    print('Latitude = n/a')
                    print('Longitude = n/a')                
                break

                
            # SQL query
            if querytosql:
                #execute insert gps sql
                #query = ("INSERT INTO gps (gpslat,gpslng,username) VALUES (%s,%s,%s)")
                #data = (data_stream.TPV['lat'], data_stream.TPV['lon'], 'car')
                #cur.execute(query, data)
                #db.commit()
                #execute insert sensor sql
                querye = ("INSERT INTO sensor (gpslat, gpslng, temperature, humidity, username) VALUES (%s,%s,%s,%s,%s)")
                sen = (data_stream.TPV['lat'], data_stream.TPV['lon'], htread.temperature, htread.humidity ,'car')
                cur.execute(querye, sen)
                db.commit()   

        sleep(0.0001)

except BaseException as inst:
    print(type(inst))
    print(inst.args)
    print(inst)
    x, y = inst.args
    print('x =', x)
    print('y =', y) 
    print("Command: FORCE STOP ", end='')
    stop()
    gpio.cleanup()
