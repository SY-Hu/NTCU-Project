import ThreadCommunication
import threading
import queue
import get_IP
import time


class printQueue(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.qlock = threading.Lock()
        self.receiveThread = ThreadCommunication.ReceiveThread(self.qlock)
        self.receiveThread.start()
        print("[Printing] Printing thread start.")

    def run(self):
        while not self._stop_event.is_set():
            ThreadCommunication.qlock.acquire()
            if not ThreadCommunication.receivedQueue.empty():
                data = ThreadCommunication.receivedQueue.get()
                print("[Test ] Receive:",data)
            ThreadCommunication.qlock.release()
               

    def stop(self):
        self._stop_event.set()

    def __del__(self):
        threading.Thread.__del__()
        ThreadCommunication.qlock.release()
        self.receiveThread.stop()
        self.receiveThread.join()
        print("[Printing] Thread end.")


print("[Test ] Test Program for ThreadCommunication")
broadcastIP = get_IP.getBroadcastIP()
print("[Test ] Broadcast IP = ",broadcastIP)

send = ThreadCommunication.SendThread(repeatFreq = 0.5)
send.start()
printThread = printQueue()
printThread.start()
#qlock = threading.Lock()
#receiveThread = ThreadCommunication.ReceiveThread(qlock)
#receiveThread.start()

command = "on"
while True:
    '''try:
        time.sleep(i)
        print("[Test ] Please input test message: (use carCommand) ->",i)
        #command  = str(input("[Test ] Command: "))
        i = i + 1
        if command == 'quit':
            break
        else:
            data = {'type':'carMaster','context':{'command':str(i)}}
            send.send(data,broadcastIP,repeat=True)
    except:
        break'''
    try:
        if command == "on":
            command = "off"
        else:
            command = "on"
        data = {'type':'sideCommand','context':{'led':{"roadlight1":command}}}
        send.send(data,broadcastIP,repeat=True)
        time.sleep(5)
    except:
        print("[Test ] Break.")
        break
   
    '''if not ThreadCommunication.receivedQueue.empty():
                #ThreadCommunication.qlock.acquire()
                data = ThreadCommunication.receivedQueue.get()
                #ThreadCommunication.qlock.release()
                print("[Test ] Receive:",data)'''

send.stop()
#receiveThread.stop()
printThread.stop()
send.join()
#receiveThread.join()
printThread.join()
    
print("[Test ] Program end.")
