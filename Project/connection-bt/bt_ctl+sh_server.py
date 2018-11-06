import socket
from gpiozero import LED
from subprocess import call

print("Socket Server - Bluetooth Control ver.")
print("Program start. Waiting for client connection.")


hostMACAddress = 'B8:27:EB:F2:4C:B9'
port = 22
backlog = 1
size = 1024
inBash = False
s = socket.socket(socket.AF_BLUETOOTH,socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((hostMACAddress,port))
s.listen(backlog)
try:
    client,address = s.accept()
    while 1:
         data = client.recv(size)
         if data:
             if not inBash:
                 if data == "on" or data == "ON":
                     call(["sudo","./openLED.sh"])
                     print("Open LED")
                     client.send("Open Led")
                 elif data == "off" or data == "OFF":
                     call(["sudo","./closeLED.sh"])
                     print("Close LED")
                     client.send("Close LED")
                 elif data == "bash":
                     inBash = True
                     print("Start bash")
                     client.send("Start bash")
                 else:
                     print data
                     client.send(data)
             else:
                 if data == "bash":
                     inBash = False
                     print("Exit bash")
                     client.send("Exit bash")
                 else:
                     call([data])
except :
      print("CLOSE SOCKET")
      client.close()
      s.close()
print("Program server end.")

