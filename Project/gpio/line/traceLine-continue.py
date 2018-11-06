from gpiozero import LineSensor
from signal import pause
from time import sleep

onLine = False
sensor = LineSensor(4)

sensor.when_line = lambda: getState(True)
sensor.when_no_line = lambda: getState(False)


def getState(data):
    global onLine
    onLine  = data
    if data:
        print("data line")
    else:
        print("data not_line")

i = 0

while True:
    i+=1
    if onLine:
        print("line")
    else:
        print("not_line")
    print ("%d times " % i)
    sleep(1)
