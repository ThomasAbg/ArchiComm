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
from client import connectClient
from Frame import run_window
from multiprocessing import Process, Queue


if __name__ == "__main__":
    q = Queue()
    p = Process(target=run_window, args=(q,))
    p.start()
    while(1):
        #attente de la recupération de date dans run_window modifier par run_window 
        dataReceive = q.get()
        print("data=", dataReceive)    # prints "[42, None, 'hello']"
        print("dataReceive[0]:", dataReceive[0])
        if(dataReceive == "close"):
            q.close()   #libert la ressource q
            p.close()   #termine le processus run_window
            break
        if(dataReceive[0] == "Connect"):
            print("Start processus client")
            p2 = Process(target=connectClient, args=(dataReceive[1],dataReceive[2]))
            p2.start()
            p.join()
            p2.join()
            
    print("Fin de la boucle principal")
    #p.join()