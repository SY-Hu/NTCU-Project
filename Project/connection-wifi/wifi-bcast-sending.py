import socket

#UDP_IP = "255.255.255.255"
UDP_IP = "192.168.43.255"
UDP_PORT = 5005

print ("Wifi UDP Sending Program")
print ("UDP target IP:", UDP_IP)
print ("UDP target port:", UDP_PORT)

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

while 1:
    text = input()
    sock.sendto(text.encode(), (UDP_IP, UDP_PORT))
    if text == 'quit':
        break

