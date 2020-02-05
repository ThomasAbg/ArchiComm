import socket


def connectClient(data_q):
    print("Client ok")
    global CLIENT
    global alive
    alive = True
    data_rcv = ""
    dataReceive = []

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

            if message.endswith(" E!§N/!D"):
                print("Free message")
                message = message[:-7]
                data_q.put(["rcv", message, ""], True)

            elif message.endswith(
                "chatµ%£=."
            ):  # detect new client in chatroom
                PseudoCco = message[:-19]
                data_q.put(["Connclient", PseudoCco])

            elif message.endswith("AAAZEZ"):
                message = message[:-6]
                lenght = int(message[-3:]) - 100
                message = message[:-3]
                listclient = message[:-lenght]
                print("listclient:", listclient)
                if lenght != 0:
                    for i in range(lenght):
                        clientco = replaceMultiple(
                            listclient.split('"')[i], ["[", "]", '"', "'"], ""
                        )
                        data_q.put(["Connclient", clientco])

            elif message.endswith(
                "discon3630."
            ):  # detect client leave chatroom
                message = message[:-15]
                data_q.put(["Discoclient", message])

            message = ""
            data_rcv = False
    CLIENT.close()

    print("Client close")


def ClientSend(data):
    byt_message = data.encode()
    CLIENT.send(byt_message)


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
