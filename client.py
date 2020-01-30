import socket
import select
import sys
import socket


CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CLIENT.setblocking(0)

def exitClient():
    global alive
    alive = False

def connectClient(data_q):
    print("Client ok")
    global alive
    alive = True
    data_rcv = ""
    dataReceive = []
    
    while alive:
        if not data_q.empty():
            dataReceive = data_q.get(False)
            break
    
    if(dataReceive[0] == "RunClient"):
        IP_address = dataReceive[1]
        Port = dataReceive[2]
        
        try:
            CLIENT.connect((IP_address, Port))
            
        except socket.gaierror as e:
            print("Address-related error connecting to CLIENT: ", e, " Fail to connect to: ", IP_address, Port)

        except socket.error as e:
            print("Connection error: ", e, " Fail to connect to: ", IP_address, Port)
        
        while alive:
            try:
                data_rcv = CLIENT.recv(2048)
            except socket.error:
                pass # no data receive
            if(not data_rcv):
                pass # no data
            else:
                message = data_rcv.decode()
                print("Message recu:", message)
                data_q.put(["rcv", message, ""], True)
                data_rcv = False
        CLIENT.close()
        print("Client close")
        
def ClientSend(data):
    byt_message = data.encode()
    CLIENT.send(byt_message)