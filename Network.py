import threading
import socket
import pygame
from pygame.locals import *


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


##############################################################
##################  KLASSENLOSER CODE  #######################
##############################################################

serverThread = ThreadedServer()
serverThread.start()




