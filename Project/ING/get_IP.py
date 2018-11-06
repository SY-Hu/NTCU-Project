import socket
def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    #print(s.getsockname()[0])
    ip = str(s.getsockname()[0])
    s.close()
    return ip

def getBroadcastIP():
    myIP = getIP()
    broadcastLastPoint = [posi for posi, char in enumerate(myIP) if char == '.']
    broadcastIP = myIP[0:broadcastLastPoint[2]] + ".255"
    return broadcastIP

