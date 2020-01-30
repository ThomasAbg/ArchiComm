#-------------------------------------------------------------------------------
# Name:        ArchiComm
# Purpose:
#
# Author:      Thomas
#
# Created:     11/01/2020
# Copyright:   (c) Thomas 2020
# Licence:     <priver>
#-------------------------------------------------------------------------------

# -*- coding: utf-8 -*-
#!/usr/bin/env python
import threading
import time
import datetime
from multiprocessing import Queue

from Frame import run_window, WriteMsgRcv
from client import connectClient, ClientSend, exitClient


status = Queue(maxsize=0)
statusClient = Queue(maxsize=0)

def running():
    statusConnect = 0
    while(1):
        if(not statusClient.empty()):
            dataReceiveClient = statusClient.get()
            print("MAIN data from Client: ", dataReceiveClient)
            if(dataReceiveClient[0] == "rcv"):
                print("dataReceiveClient: ", dataReceiveClient[1])
                WriteMsgRcv(dataReceiveClient[1])
        
        elif(not status.empty()):
            dataReceive = status.get()
            print("MAIN data from Frame: ", dataReceive)    # prints "[42, None, 'hello']"
            
            if(dataReceive[0] == "Connect"):
                print("Start processus client")
                statusClient.put(["RunClient", dataReceive[1], dataReceive[2]], True)
                statusConnect = 1
            
            if(dataReceive[0] == "text" and statusConnect == 1):
                ClientSend(dataReceive[1])
            elif(dataReceive[0] == "text" and statusConnect == 0):
                print("Try to send data but not connected to server at ", datetime.datetime.now())
                
            if(dataReceive == "exit"):
                exitClient()
                print("Main close")
                break
        
        else:
            time.sleep(0.1)

thread1 = threading.Thread(target = running, args=())
thread1.start()
thread2 = threading.Thread(target = connectClient, args=(statusClient, ))
thread2.start()

run_window(status)

print("step1")
thread1.join()
print("step2")
thread2.join()
print("step4")
status.close()
print("step5")
statusClient.close()

print("All threads close")
