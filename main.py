# -------------------------------------------------------------------------------
# Name:        ArchiComm
# Purpose:
#
# Author:      Thomas
#
# Created:     11/01/2020
# Copyright:   (c) Thomas 2020
# Licence:     <priver>
# -------------------------------------------------------------------------------

# -*- coding: utf-8 -*-
#!/usr/bin/env python
import threading
import time
import datetime
from multiprocessing import Queue

from Frame import run_window, WriteMsgRcv, addClient, removeClient
from client import connectClient, ClientSend, exitClient


status = Queue(maxsize=0)
statusClient = Queue(maxsize=0)


def running():
    global statusConnect
    statusConnect = 0
    while 1:
        if not statusClient.empty():
            dataReceiveClient = statusClient.get()
            print("Sys msg from Client: ", dataReceiveClient)
            if dataReceiveClient[0] == "rcv":
                print("dataReceiveClient: ", dataReceiveClient[1])
                WriteMsgRcv(dataReceiveClient[1])
            elif dataReceiveClient[0] == "Connclient":
                addClient(dataReceiveClient[1])
            elif dataReceiveClient[0] == "Discoclient":
                removeClient(dataReceiveClient[1])

        elif not status.empty():
            dataReceive = status.get()
            print("Sys msg from Frame: ", dataReceive)

            if dataReceive[0] == "Connect":
                print("Start processus client")
                statusClient.put(
                    [
                        "RunClient",
                        dataReceive[1],
                        dataReceive[2],
                        dataReceive[3],
                    ],
                    True,
                )
                statusConnect = 1

            if dataReceive[0] == "text" and statusConnect == 1:
                ClientSend(dataReceive[1])
            elif dataReceive[0] == "text" and statusConnect == 0:
                print(
                    "Try to send data but not connected to server at ",
                    datetime.datetime.now(),
                )

            if dataReceive == "exit":
                if statusConnect == 1:
                    ClientSend(99, "")
                exitClient()
                print("Main close")
                break
        else:
            time.sleep(0.1)


thread1 = threading.Thread(target=running, args=())
thread1.start()
thread2 = threading.Thread(target=connectClient, args=(statusClient,))
thread2.start()

run_window(status)

# Closing
thread1.join()
thread2.join()
status.close()
statusClient.close()

# Sous Windows il faut mettre ce programme en pause (inutile sous Linux)
# os.system("pause")

print("All threads close")
