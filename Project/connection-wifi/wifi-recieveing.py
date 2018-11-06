import socket

#UDP_IP = "192.168.2.106"
#UDP_IP = "127.0.0.1"
UDP_IP = "Receiveing"

UDP_PORT = 5005

print ("Wifi UDP Recieveing Program")
print ("UDP target IP:", UDP_IP)
print ("UDP target port:", UDP_PORT)

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind(('', UDP_PORT))
try:
    while 1:
        #text=sock.recv(4096).decode()
        receive = sock.recvfrom(4096)
        print(receive)
        if receive[0].decode() == 'quit':
            break
except:
    pass
