import socket
from thread import *
import sys


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
"""
the first argument AF_INET is the address domain of the socket. This is used when we have an Internet Domain
with any two hosts
The second argument is the type of socket. SOCK_STREAM means that data or characters are read in a continuous flow
"""
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.bind((IP_address, Port))
# binds the server to an entered IP address and at the specified port number. The client must be aware of these parameters
server.listen(100)
# listens for 100 active connections. This number can be increased as per convenience
list_of_clients = []


def clientthread(conn, addr):
    while True:
        try:
            data_rcv = conn.recv(2048)
            message = data_rcv.decode()
            if message:
                if message[0:7] == "Pseudo:":
                    Pseudo = message[7:16]
                    print(addr[0] + ": " + Pseudo + " connected")
                    msg = "Welcome to this chatroom " + Pseudo + " !"
                    msg_enc = msg.encode()
                    conn.send(msg_enc)
                elif message == "Leave":
                    msg = Pseudo + " have leave the chatroom."
                    broadcast(msg, conn)
                else:
                    # prints the message and address of the user who just sent the message on the server terminal
                    print("<" + addr[0] + "> " + message)
                    message_to_send = "<" + addr[0] + "> " + message.encode()
                    broadcast(message_to_send, conn)
            else:
                remove(conn)
        except:
            continue


def broadcast(message, connection):
    for clients in list_of_clients:
        print("client:", clients, "et connection:", connection)
        if clients != connection:
            print("client != ", connection)
            try:
                print("send msg")
                clients.send(message)
            except:
                print(clients," Leave")
                clients.close()
                remove(clients)


def remove(connection):
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
    start_new_thread(clientthread, (conn, addr))
    # creates and individual thread for every user that connects


conn.close()
server.close()
