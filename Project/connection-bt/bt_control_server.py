import socket
from gpiozero import LED
from subprocess import call

print("Socket Server - Bluetooth Control ver.")
print("Program start. Waiting for client connection.")


hostMACAddress = 'B8:27:EB:F2:4C:B9'
port = 22
backlog = 1
size = 1024
s = socket.socket(socket.AF_BLUETOOTH,socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((hostMACAddress,port))
s.listen(backlog)
try:
    client,address = s.accept()
    while 1:
         data = client.recv(size)
         if data:
             print(data)
             client.send(data)
         if data == "on" or data == "ON":
             call(["sudo","./openLED.sh"])
         if data == "off" or data == "OFF":
             call(["sudo","./closeLED.sh"])
except :
      print("CLOSE SOCKET")
      client.close()
      s.close()
print("Program server end.")

