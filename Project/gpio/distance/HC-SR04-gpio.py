from gpiozero import DistanceSensor
from time import sleep

echo = 6
trigger = 12

sensor = DistanceSensor(echo, trigger)
while True:
    print('Distance: ', sensor.distance * 100)
    sleep(0.1)
