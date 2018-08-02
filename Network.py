import threading
import socket
<<<<<<< HEAD
# import threading
import pygame
from pygame.locals import *

=======
import time
from enum import Enum
import uuid
>>>>>>> b51c0938f6048bd704fe9bfb70ff8093da28eeaf

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

<<<<<<< HEAD
pygame.init()


class Player:
    recX = None
    recY = None
    #speed = None
    recWidth = None
    recHeight = None
    blue = (0, 0, 255)


    def __init__(self, recX, recY):
        self.recX = recX
        self.recY = recY
        self.recWidth = 85
        self.recHeight = 85
        game = Game()
        display = game.get_gameDisplay()
        #self.speed = speed
        #pygame.draw.rect(Game.gameDisplay, self.blue, (recX, recY, self.recWidth, self.recHeight))

    def draw(self):
        pygame.draw.rect(Game.gameDisplay, self.blue, (self.recX, self.recY, self.recWidth, self.recHeight))

    # def run(self):
    #
    #
    # def hit(self):

class Game:
    displayWidth = 1200
    displayHeight = 600

    black = (0, 0, 0)
    white = (255, 255, 255)

    gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
    pygame.draw.rect(gameDisplay, black, (200, 150, 100, 50))
    gameDisplay.fill(white)
    pygame.display.set_caption('Double Crossing')

    player = Player(200, 200)
    player.draw();

    def get_gameDisplay(self):
        return self.gameDisplay

    def gameLoop():
        while True:
            for event in pygame.event.get():

                if event.type == QUIT:
                    pygame.quit()
                    quit()
            pygame.display.update()


    gameLoop()

=======
    LEFT = None
    RIGHT = None
    UP = None
    DOWN = None
    SPACE = None

class KEYUP(Enum):

    LEFT = None
    RIGHT = None
    UP = None
    DOWN = None
    SPACE = None

class PLAYERCOMMAND():

    def __init__(self, ID, KEYEVENTS):
        self.ID = ID
        self.KEYEVENTS = KEYEVENTS

    ID = None
    KEYEVENTS = None
>>>>>>> b51c0938f6048bd704fe9bfb70ff8093da28eeaf

##############################################################
##################  KLASSENLOSER CODE  #######################
##############################################################


serverThread = ThreadedServer()
serverThread.start()

<<<<<<< HEAD



=======
>>>>>>> b51c0938f6048bd704fe9bfb70ff8093da28eeaf
