import socket


def connectClient(data_q):
    print("Client ok")
    global CLIENT
    global alive
    alive = True
    data_rcv = ""
    dataReceive = []
    message = ""

    # process connection
    while alive:
        if not data_q.empty():
            dataReceive = data_q.get(False)

            if dataReceive[0] == "RunClient":
                CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                CLIENT.setblocking(0)
                CLIENT.settimeout(10)
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
                    ClientSend(10, Pseudo)
                    print("We are CONNECT")
                    break
                else:
                    print("error has catch")

    # process connection done, life of communication
    while alive:
        try:
            data_rcv = CLIENT.recv(2048)
        except OSError:
            pass  # no data receive
        if data_rcv:
            # message = data_rcv.decode()
            data_rcv[0]
            lenght = data_rcv[1]
            print("ID receive:", data_rcv[0])
            print("lenght receive:", data_rcv[1])
            for i in range(lenght + 1):
                message += chr(data_rcv[i + 2])
            message = message[1:]
            print("Message rcv:", message)

            # receive new classique message
            if data_rcv[0] == 1:
                data_q.put(["rcv", message, ""], True)

            # receive new client connect in chatroom
            elif data_rcv[0] == 2:
                print("message for 2:", message)
                pseudos = message.split(",")
                print("pseudos:", pseudos)
                for pseudo in pseudos:
                    if pseudo != "":
                        print("pseudo[", i, "]=", pseudo)
                        data_q.put(["Connclient", pseudo])

            # receive list currently connected client
            elif data_rcv[0] == 3 and lenght != 0:
                print("MESSAGE3:", message, type(message))
                data_q.put(["Connclient", message])

            # detect client leave chatroom
            elif data_rcv[0] == 99:
                data_q.put(["Discoclient", message])

            message = ""
            data_rcv = False

    CLIENT.close()
    print("Client close")


def ClientSend(code: int, data: str):
    global CLIENT
    bytesmsg = bytearray(3)
    bytesmsg[0] = code
    bytesmsg[1] = len(data)
    bytesmsg.extend(data.encode())
    CLIENT.send(bytesmsg)


# replaceMultiple(list[i], ["[", "]", '"', "'"], "")
def replaceMultiple(mainString, toBeReplaces, newString):
    # Iterate over the strings to be replaced
    for elem in toBeReplaces:
        # Check if string is in the main string
        if elem in mainString:
            # Replace the string
            mainString = mainString.replace(elem, newString)

    return mainString


def exitClient():
    global alive
    alive = False
