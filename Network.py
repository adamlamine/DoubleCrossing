import threading
import socket
import time
from enum import Enum
import uuid
from base64 import b64encode
from hashlib import sha1

import pygame as pygame


class ThreadedServer(threading.Thread):

    IP = "127.0.0.1"
    port = 5555

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IP, port))
    s.listen(5)

    clientList = []
    cmdQueue = []

    def getCmdQueue(self):
        temp = self.cmdQueue
        self.cmdQueue = []
        return temp

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
            self.handshake(connection)

            self.clientList.append(ThreadedClient(address, connection, uuid.uuid4())) #initialisiert den ClientThread mit einer unique ID
            self.clientList[len(self.clientList)-1].start()

            print("Verbindung mit " + str(address) + " hergestellt.")

    def handshake(self, connection):

        GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11" #festgelegter String, der fuer Handshake an key appended wird

        data = connection.recv(2048)
        msg = data.decode('latin-1')

        startIndex = msg.find("WebSocket-Key: ") + len("WebSocket-Key: ")
        endIndex = msg.find("Sec-WebSocket-Extensions:") - 1
        key = msg[startIndex:endIndex]
        key = key.replace('\r', '')


        processedKey = b64encode(sha1( (key + GUID).encode('utf-8') ).digest())

        response =  "HTTP/1.1 101 Switching Protocols\r\n"
        response += "Upgrade: websocket\r\n"
        response += "Connection: Upgrade\r\n"
        response += "Sec-WebSocket-Accept: " + processedKey.decode("utf-8") + "\r\n\r\n"

        print(response)

        connection.send(bytes(response, 'utf-8'))

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

    def decodeFrame(self, frame):
        #############TODO: Verstehen

        opcode_and_fin = frame[0]

        payload_len = frame[1] - 128

        mask = frame[2:6]
        encrypted_payload = frame[6: 6 + payload_len]

        payload = bytearray([encrypted_payload[i] ^ mask[i % 4] for i in range(payload_len)])

        return payload

    def inputLoop(self):
        while True:
            try:
                frame = self.connection.recv(2048)
                msg = self.decodeFrame(frame).decode()
                print(msg)

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

            try:
                data = self.connection.recv(2048, socket.MSG_PEEK)

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

    LEFT = "LEFT_DOWN"
    RIGHT = "RIGHT_DOWN"
    UP = "UP_DOWN"
    DOWN = "DOWN_DOWN"
    SPACE = "SPACE_DOWN"

class KEYUP(Enum):

    LEFT = "LEFT_UP"
    RIGHT = "RIGHT_UP"
    UP = "UP_UP"
    DOWN = "DOWN_UP"
    SPACE = "SPACE_UP"

class PLAYERCOMMAND():

    def __init__(self, ID, KEYEVENT):
        self.ID = ID
        self.KEYEVENT = KEYEVENT

    ID = None
    KEYEVENT = None


pygame.init()

class Player:
    recX = None
    recY = None
    speed = None
    recWidth = None
    recHeight = None
    blue = (0, 0, 255)
    display = None
    solidFill = 0
    keyboardInput = pygame.key.get_focused()


    def __init__(self, recX, recY, game):
        self.recX = recX
        self.recY = recY
        self.recWidth = 85
        self.recHeight = 85
        self.display = game.get_gameDisplay()
        self.jumping = False
        self.jumpOffset = 0
        # pygame.draw.rect(Game.gameDisplay, self.blue, (recX, recY, self.recWidth, self.recHeight))

    def set_display(self):
        global display

    def set_speed(self):
        global speed

    def set_keyboardInput(self):
        global keyboardInput

    def set_recX(self):
        global recX

    def set_recY(self):
        global recY

    def set_solidFill(self):
        global solidFill

    def draw(self) -> object:
        pygame.draw.rect(self.display, self.blue, (self.recX, self.recY, self.recWidth, self.recHeight))

    def run(self, Player):
        # keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    recX += speed
                elif event.key == pygame.K_LEFT:
                    recX -= speed
                elif event.key == pygame.K_UP:
                    #TODO up key
                    pass


class Game:
    displayWidth = None
    halfWidth = None
    displayHeight = None
    halfHeight = None
    fps = None

    black = None
    white = None

    gameDisplay = None
    clock = None

    player = None


    def __init__(self):
        self.displayWidth = 1200
        self.halfWidth = self.displayWidth / 2
        self.displayHeight = 600
        self.halfHeight = self.displayHeight / 2
        self.fps = 200

        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

        self.gameDisplay = pygame.display.set_mode((self.displayWidth, self.displayHeight))
        pygame.draw.rect(self.gameDisplay, self.black, (200, 150, 100, 50))
        self.gameDisplay.fill(self.white)
        pygame.display.set_caption('Double Crossing')
        self.clock = pygame.time.Clock()

        self.player = Player(self.halfWidth, self.halfHeight, self)
        self.player.draw()

    def set_clock(self):
        global clock

    def set_fps(self):
        global fps

    def set_gameDisplay(self, gameDisplay):
        self.gameDisplay = gameDisplay

    def get_gameDisplay(self):
        return self.gameDisplay

    def gameLoop(self):
        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            pygame.display.update()

            self.clock.tick(self.fps)




##############################################################
################  KLASSENLOSER CODE ADAM  ####################
##############################################################


serverThread = ThreadedServer()
serverThread.start()


##############################################################
################  KLASSENLOSER CODE CARO  ####################
##############################################################

game = Game()
game.gameLoop()
