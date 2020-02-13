# -------------------------------------------------------------------------------
# Name:        ArchiComm
# Purpose:
#
# Author:      Thomas
#
# Created:     11/01/2020
# Copyright:   (c) Thomas 2020
# Licence:     <>
# -------------------------------------------------------------------------------

# -*- coding: utf-8 -*-
# !/usr/bin/env python

"""Code server chatroom TCP."""

import socket
import threading
import sys
import time
import datetime
import simplelogging
from typing import List

log = simplelogging.get_logger()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
"""
the first argument AF_INET is the address domain of the socket.
This is used when we have an Internet Domain with any two hosts.
The second argument is the type of socket. SOCK_STREAM means that
data or characters are read in a continuous flow
"""
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.bind((IP_address, Port))
# binds the server to an entered IP address and at the specified port number.
# The client must be aware of these parameters
server.listen(100)
# listens for 100 active connections.
# This number can be increased as per convenience
list_of_clients: List[socket.socket] = []
list_of_pseudo = []


def clientthread(conn, addr):
    """Control Main of the threads."""
    message = ""
    Pseudo = ""
    while True:
        try:
            data_rcv = conn.recv(2048)
            if data_rcv:
                ID = int(data_rcv[0])
                print("ID=", ID)
                lenght = int(data_rcv[1])
                message = ""
                for i in range(lenght):
                    message += chr(data_rcv[3 + i])
                if ID == 10:
                    treatmentConnection(conn, addr)
                elif ID == 11:
                    Pseudo = receivepseudo(conn, addr, message)
                elif ID == 99:
                    treatmentDisconnection(conn, addr, Pseudo)
                elif ID == 7:
                    # prints the message and address of the user who just sent
                    # the message on the server terminal
                    print(
                        datetime.datetime.now(),
                        " ",
                        "<" + addr[0] + "> " + Pseudo + ": " + message,
                    )
                    message_to_send = Pseudo + ": " + message
                    bytesmsg = bytearray(3)
                    bytesmsg[0] = 1
                    bytesmsg[1] = len(message_to_send)
                    bytesmsg.extend(map(ord, message_to_send))
                    sendmsg(bytesmsg, conn, 1)
            """else:
                remove(conn)"""
        except:
            continue


def treatmentConnection(conn, addr):
    """Treat new client connection."""
    # ##### send pseudo list to the new client ######
    lenght = 0
    bytesmsg = bytearray(3)
    bytesmsg[0] = 2
    if list_of_pseudo != []:
        for element in list_of_pseudo:
            lenght += len(element)
    bytesmsg[1] = lenght
    i = 2
    for pseudoelem in list_of_pseudo:
        pseudoelem = pseudoelem + ","
        bytesmsg[1] += 1  # add "," in the lenght of message
        bytesmsg.extend(bytearray(pseudoelem, "utf-8"))
        i += 1
    sendmsg(bytesmsg, conn, modebroadcast=False)
    bytesmsg = bytearray(3)


def receivepseudo(conn, addr, Pseudo):
    # ##### send the welcome message ######
    lenght = 0
    log.info("<" + addr[0] + "> " + ": " + Pseudo + " connected")
    msg = "Welcome to this chatroom " + Pseudo + " !"
    test = bytes(msg, "utf8")
    bytesmsg = bytearray(3)
    bytesmsg[0] = 1
    bytesmsg[1] = len(test)
    bytesmsg.extend(map(ord, msg))
    sendmsg(bytesmsg, conn, modebroadcast=False)
    bytesmsg = bytearray(3)

    # ##### send who join to everyone ######
    msg = Pseudo
    bytesmsg[0] = 3
    bytesmsg[1] = len(Pseudo)
    bytesmsg.extend(Pseudo.encode())
    sendmsg(bytesmsg, conn, modebroadcast=True)
    list_of_pseudo.append(Pseudo)
    log.info("List pseudo:%s", list_of_pseudo)
    bytesmsg = bytearray(3)

    return Pseudo


def treatmentDisconnection(conn, addr, message):
    """Treat for disconneection of a client."""
    print("APPEL")
    bytesmsg = bytearray(3)
    bytesmsg[0] = 99
    bytesmsg[1] = len(message)
    bytesmsg.extend(message.encode())
    print("bytesmsg:", bytesmsg)
    sendmsg(bytesmsg, conn, 1)
    list_of_pseudo.remove(message)  # remove client of pseudo list
    print("Client:", message, "disconnected")


def sendmsg(message: bytearray, connection, modebroadcast):
    """
        function to send message in broadcast or not
    """
    # message = message.encode("utf8")
    # broadcast send to everyone expect transmitter
    for clients in list_of_clients:
        if modebroadcast:
            if clients != connection:
                try:
                    clients.send(message)
                except:
                    print(datetime.datetime.now(), " ", clients, " Leave")
                    clients.close()
                    remove(clients)
        elif clients == connection:  # mode private message
            print("MESSAGE SEND:", message)
            clients.send(message)
            break


def remove(connection):
    """Remove client connection of the list of connection."""
    if connection in list_of_clients:
        list_of_clients.remove(connection)


while True:
    conn, addr = server.accept()
    """
    Accepts a connection request and stores two parameters, conn which is a socket object for that user, and addr which contains
    the IP address of the client that just connected
    """

    list_of_clients.append(conn)

    # maintains a list of clients for ease of broadcasting a message to all available people in the chatroom
    # Prints the address of the person who just connected
    threading._start_new_thread(clientthread, (conn, addr))
    # creates and individual thread for every user that connects

conn.close()
server.close()
