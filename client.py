import socket
import select
import sys
import socket

alive = True


CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CLIENT.setblocking(0)

def exitClient():
    alive = False
    print("CHANGE alive")

def connectClient(data_q):
    print("Client ok")
    dataReceive = data_q.get()
    data_rcv = ""
    
    if(dataReceive[0] == "RunClient"):
        global alive
        alive = True
        IP_address = dataReceive[1]
        Port = dataReceive[2]
        
        try:
            CLIENT.connect((IP_address, Port))
            
        except socket.gaierror as e:
            print("Address-related error connecting to CLIENT: ", e, " Fail to connect to: ", IP_address, Port)

        except socket.error as e:
            print("Connection error: ", e, " Fail to connect to: ", IP_address, Port)
        
        PourComm = data_q
        while alive:
            try:
                data_rcv = CLIENT.recv(2048)
            except socket.error:
                print("no rcv")
            if(not data_rcv):
                print("No data")
            else:
                message = data_rcv.decode()
                print("Message recu:", message)
                PourComm.put(["rcv", message, ""], True)
                data_rcv = False
            print("alive =", alive)
            if(alive == False):
                break
        CLIENT.close()
        print("Client close")
    print("Bye client")
    
def ClientSend(data):
    byt_message = data.encode()
    CLIENT.send(byt_message)