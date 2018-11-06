import socket

print("Socket Client - Bluetooth ver.")
print("Program start. Try type some words.")

serverMACAddress = 'B8:27:EB:F2:4C:B9'
port = 22
s = socket.socket(socket.AF_BLUETOOTH,socket.SOCK_STREAM,socket.BTPROTO_RFCOMM)
s.connect((serverMACAddress,port))
while 1:
    text = input()
    if text == 'quit':
        break
    s.send(bytes(text,'UTF-8'))
s.close()

print("Program client end.")
