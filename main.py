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

from multiprocessing import Process, Queue
from client import connectClient
from Frame import run_window, WriteMsgRcv

if __name__ == "__main__":
    q = Queue()
    p = Process(target=run_window, args=(q,))
    p.start()
    while(1):
        dataReceive = q.get()
        print("data=", dataReceive)    # prints "[42, None, 'hello']"
        if(dataReceive[0] == "close"):
            q.close()   #libert la ressource q
            p.close()   #termine le processus run_window
            break
        if(dataReceive[0] == "Connect"):
            print("Start processus client")
            p2 = Process(target=connectClient, args=(dataReceive[1], dataReceive[2], q))
            p2.start()
            p.join()
            p2.join()
        if(dataReceive[0] == "rcv"):
            print("DataToSend: ", dataReceive)
            WriteMsgRcv(dataReceive[1])
            
    print("Fin de la boucle principal")