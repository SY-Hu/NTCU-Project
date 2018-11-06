import socket

UDP_IP = "192.168.43.73"
#UDP_IP = "127.0.0.1"
UDP_PORT = 5005

print ("Wifi UDP Sending Program")
print ("UDP target IP:", UDP_IP)
print ("UDP target port:", UDP_PORT)

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

while 1:
    text = input()
    sock.sendto(text.encode(), (UDP_IP, UDP_PORT))
    if text == 'quit':
        break

