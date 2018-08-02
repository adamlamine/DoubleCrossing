import threading
import socket

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
        self.clientList.remove(client)


    def serverLoop(self):

        while True:
            connection, address = self.s.accept()

            self.clientList.append(ThreadedClient(address, connection))
            self.clientList[len(self.clientList-1)].start()

class ThreadedClient(threading.Thread):

    ID = None
    address = None
    connection = None

    def __init__(self, address, connection):
        self.address = address
        self.connection = connection
        threading.Thread.__init__(self)

    def run(self):
        self.inputLoop()

    def inputLoop(self):
        while True:
            self.connection.recv(1024)


##############################################################
##################  KLASSENLOSER CODE  #######################
##############################################################

serverThread = ThreadedServer()
serverThread.start()