import socket
import select
import socket
import time

CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CLIENT.setblocking(0)


def connectClient(data_q):
    print("Client ok")
    global alive
    alive = True
    data_rcv = ""
    dataReceive = []

    while alive:
        if not data_q.empty():
            dataReceive = data_q.get(False)

            if dataReceive[0] == "RunClient":
                IP_address = dataReceive[1]
                Port = dataReceive[2]
                Pseudo = dataReceive[3]
                catcherror = 0

                try:
                    CLIENT.connect((IP_address, Port))

                except socket.gaierror as e:
                    print(
                        "Address-related error connecting to CLIENT: ",
                        e,
                        " Fail to connect to: ",
                        IP_address,
                        Port,
                    )
                    catcherror = 1

                except OSError as e:
                    print(
                        "Connection error: ",
                        e,
                        " Fail to connect to: ",
                        IP_address,
                        Port,
                    )
                    catcherror = 1

                if catcherror == 0:
                    ClientSend("P%µudo:" + Pseudo)
                    print("We are CONNECT")
                    break
                else:
                    print("error has catch")

    while alive:
        try:
            data_rcv = CLIENT.recv(2048)
        except OSError:
            pass  # no data receive
        if data_rcv:
            message = data_rcv.decode()
            print("Message recu:", message)
            if message.endswith("chatµ%£=."): # detect new client in chatroom
                message = message[:-19]
                data_q.put(["Connclient", message])
            elif(message.endswith("discon3630.")): # detect client leave chatroom
                message = message[:-15]
                data_q.put(["Discoclient", message])
            else:
                data_q.put(["rcv", message, ""], True)
            data_rcv = False
    CLIENT.close()
   
    print("Client close")


def ClientSend(data):
    byt_message = data.encode()
    CLIENT.send(byt_message)

def exitClient():
    global alive
    alive = False

