import socket

UDP_IP = "192.168.43.73"
#UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = "Hello, World!"

print ("UDP target IP:", UDP_IP)
print ("UDP target port:", UDP_PORT)
print ("message:", MESSAGE)
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.sendto(bytes(MESSAGE,'UTF-8'), (UDP_IP, UDP_PORT))
