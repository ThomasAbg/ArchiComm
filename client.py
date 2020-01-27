import socket
import select
import sys

''' 
if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2]) '''

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connectClient(data_q):
    print("Client ok")
    dataReceive = data_q.get()
    print("Info ac=", dataReceive)    # prints "[42, None, 'hello']"
    if(dataReceive[0] == "RunClient"):
        IP_address = dataReceive[1]
        Port = dataReceive[2]
        server.connect((IP_address, Port))
        PourComm = data_q
        while True:
            sockets_list = [sys.stdin, server]
            read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])
            for socks in read_sockets:
                if socks == server:
                    data_rcv = socks.recv(2048)
                    message = data_rcv.decode()
                    print("Message recu: ", message)
                    PourComm.put(["rcv", message, ""], True)
                else:
                    dataReceive = PourComm.get()
                    if(dataReceive[0] == "text"):
                        byt_message = dataReceive[1].encode()
                        server.send(byt_message)
                        dataReceive = []
                        
        server.close()