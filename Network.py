import threading
import socket
import time
from enum import Enum
import uuid

class ThreadedServer(threading.Thread):

    IP = "127.0.0.1"
    port = 5555

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IP, port))
    s.listen(5)

    clientList = []
    cmdQueue = []

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        self.serverLoop()

    def removeClient(self, client):
        print(self.clientList[0])
        print(client)

    def serverLoop(self):

        while True:
            connection, address = self.s.accept()

            self.clientList.append(ThreadedClient(address, connection, uuid.uuid4())) #initialisiert den ClientThread mit einer unique ID
            self.clientList[len(self.clientList)-1].start()

            print("Verbindung mit " + str(address) + " hergestellt.")

class ThreadedClient(threading.Thread):

    ID = None
    address = None
    connection = None

    def __init__(self, address, connection, ID):
        self.address = address
        self.connection = connection
        self.ID = ID
        threading.Thread.__init__(self)

    def run(self):
        inputThread = threading.Thread(target=self.inputLoop)
        stillaliveThread = threading.Thread(target=self.stillaliveLoop, args=(self, ))
        inputThread.start()
        stillaliveThread.start()

    def inputLoop(self):
        while True:
            try:
                data = self.connection.recv(1024)
                msg = data.decode('latin-1')

                if "KEYDOWN: LEFT" in msg:
                    serverThread.cmdQueue.append(PLAYERCOMMAND(self.ID,KEYDOWN.LEFT ))
                if "KEYDOWN: RIGHT" in msg:
                    serverThread.cmdQueue.append(PLAYERCOMMAND(self.ID,KEYDOWN.RIGHT ))
                if "KEYDOWN: UP" in msg:
                    serverThread.cmdQueue.append(PLAYERCOMMAND(self.ID,KEYDOWN.RIGHT ))
                if "KEYDOWN: DOWN" in msg:
                    serverThread.cmdQueue.append(PLAYERCOMMAND(self.ID,KEYDOWN.RIGHT ))
                if "KEYDOWN: SPACE" in msg:
                    serverThread.cmdQueue.append(PLAYERCOMMAND(self.ID,KEYDOWN.RIGHT ))


                if "KEYUP: LEFT" in msg:
                    serverThread.cmdQueue.append(PLAYERCOMMAND(self.ID,KEYDOWN.LEFT ))
                if "KEYUP: RIGHT" in msg:
                    serverThread.cmdQueue.append(PLAYERCOMMAND(self.ID,KEYDOWN.RIGHT ))
                if "KEYUP: UP" in msg:
                    serverThread.cmdQueue.append(PLAYERCOMMAND(self.ID,KEYDOWN.RIGHT ))
                if "KEYUP: DOWN" in msg:
                    serverThread.cmdQueue.append(PLAYERCOMMAND(self.ID,KEYDOWN.RIGHT ))
                if "SPACE" in msg:
                    serverThread.cmdQueue.append(PLAYERCOMMAND(self.ID,KEYDOWN.RIGHT ))

            except:
                 pass

    def stillaliveLoop(self, client):
        while True:
            time.sleep(1)
            print(len(serverThread.clientList))
            try:
                data = self.connection.recv(1024, socket.MSG_PEEK)

                if not data:
                    print("Verbindung mit " + str(self.address) + " getrennt.")
                    self.connection.close()
                    serverThread.clientList.remove(client)
                    break;

            except:
                print("Verbindung mit " + str(self.address) + " getrennt.")
                self.connection.close()
                serverThread.removeClient(client)
                break;

    def addToQueue(self, cmd):
        serverThread.cmdQueue.append(cmd)

class KEYDOWN(Enum):

    LEFT = "LEFT"
    RIGHT = "RIGHT"
    UP = "UP"
    DOWN = "DOWN"
    SPACE = "SPACE"

class KEYUP(Enum):

    LEFT = "LEFT"
    RIGHT = "RIGHT"
    UP = "UP"
    DOWN = "DOWN"
    SPACE = "SPACE"

class PLAYERCOMMAND():

    def __init__(self, ID, KEYEVENT):
        self.ID = ID
        self.KEYEVENT = KEYEVENT

    ID = None
    KEYEVENT = None


##############################################################
##################  KLASSENLOSER CODE  #######################
##############################################################


serverThread = ThreadedServer()
serverThread.start()

