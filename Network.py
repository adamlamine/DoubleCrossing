import threading
import socket
import time
from enum import Enum
import uuid
from base64 import b64encode
from hashlib import sha1



class ThreadedServer(threading.Thread):

    IP = "192.168.0.24"
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
        self.clientList.remove(client)

    def serverLoop(self):

        while True:
            connection, address = self.s.accept()
            self.handshake(connection)

            self.clientList.append(ThreadedClient(address, connection, str(uuid.uuid4())))  #initialisiert den ClientThread mit einer unique ID
            self.clientList[len(self.clientList)-1].start()

            print("Verbindung mit " + str(address) + " hergestellt.")
            print("Verbundene Clients: " + str(netModule.getPlayerCount()))

    def handshake(self, connection):

        GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11" #festgelegter String, der fuer Handshake an key appended wird

        data = connection.recv(2048)
        msg = data.decode('latin-1')

        startIndex = msg.find("WebSocket-Key: ") + len("WebSocket-Key: ")
        endIndex = msg.find("Sec-WebSocket-Extensions:") - 1
        key = msg[startIndex:endIndex]
        key = key.replace('\r', '')


        processedKey = b64encode(sha1( (key + GUID).encode('utf-8') ).digest())

        response = "HTTP/1.1 101 Switching Protocols\r\n"
        response += "Upgrade: websocket\r\n"
        response += "Connection: Upgrade\r\n"
        response += "Sec-WebSocket-Accept: " + processedKey.decode("utf-8") + "\r\n\r\n"


        connection.send(bytes(response, 'utf-8'))

    def sendToAll(self, msg):
        for i in self.clientList:
            try:
                i.sendMsg(msg.encode('utf-8'))
            except:
                pass



class ThreadedClient(threading.Thread):

    ID = None
    address = None
    connection = None

    timeToLive = 3
    alive = True

    def __init__(self, address, connection, ID):
        self.timeToLive = 3
        self.address = address
        self.connection = connection
        self.ID = ID
        netModule.onPlayerConnect(ID)
        threading.Thread.__init__(self)

    def run(self):
        inputThread = threading.Thread(target=self.inputLoop, args=(self, ))
        inputThread.start()
        TTLThread = threading.Thread(target=self.countDownTimeout, args=(self, ))
        TTLThread.start()

    def decodeFrame(self, frame):
        #############TODO: Verstehen
        #############https://superuser.blog/websocket-server-python/

        opcode_and_fin = frame[0]

        payload_len = frame[1] - 128

        mask = frame[2:6]
        encrypted_payload = frame[6: 6 + payload_len]

        payload = bytearray([encrypted_payload[i] ^ mask[i % 4] for i in range(payload_len)])

        return payload

    def sendMsg(self, payload):
        # setting fin to 1 and opcpde to 0x1
        frame = [129]
        # adding len. no masking hence not doing +128
        frame += [len(payload)]
        # adding payload
        frame_to_send = bytearray(frame) + payload

        self.connection.send(frame_to_send)

    def inputLoop(self, client):
        while self.alive:
            try:
                frame = self.connection.recv(100)
                msg = self.decodeFrame(frame).decode()
                #print(msg)
                cmd = None

                if "STILL ALIVE" in msg:
                    self.refreshTTL()

                if "PLAYERCOMMAND: " in msg:

                    if "LEFT_DOWN" in msg:
                        cmd = PLAYERCOMMAND(self.ID, KEYPRESS.LEFT)
                    if "RIGHT_DOWN" in msg:
                        cmd = PLAYERCOMMAND(self.ID, KEYPRESS.RIGHT)
                    if "UP_DOWN" in msg:
                        cmd = PLAYERCOMMAND(self.ID, KEYPRESS.UP)
                    if "DOWN_DOWN" in msg:
                        cmd = PLAYERCOMMAND(self.ID, KEYPRESS.DOWN)
                    if "SPACE_DOWN" in msg:
                        cmd = PLAYERCOMMAND(self.ID, KEYPRESS.SPACE)


                    if "LEFT_UP" in msg:
                        cmd = PLAYERCOMMAND(self.ID, KEYRELEASE.LEFT)
                    if "RIGHT_UP" in msg:
                        cmd = PLAYERCOMMAND(self.ID, KEYRELEASE.RIGHT)
                    if "UP_UP" in msg:
                        cmd = PLAYERCOMMAND(self.ID, KEYRELEASE.UP)
                    if "DOWN_UP" in msg:
                        cmd = PLAYERCOMMAND(self.ID, KEYRELEASE.DOWN)
                    if "SPACE_UP" in msg:
                        cmd = PLAYERCOMMAND(self.ID, KEYRELEASE.SPACE)

                    if cmd is not None:
                        serverThread.cmdQueue.append(cmd)
                        #TODO: Framing

                        if cmd.KEYEVENT in KEYPRESS:
                            netModule.onKeyPress(cmd)
                        if cmd.KEYEVENT in KEYRELEASE:
                            netModule.onKeyRelease(cmd)

            except UnicodeDecodeError as e:
                break

    def addToQueue(self, cmd):
        serverThread.cmdQueue.append(cmd)

    # def sendMsg(self, msg):
    #     self.connection.send(bytes(msg, 'utf-8'))

    def countDownTimeout(self, client):
        while self.alive:
            time.sleep(0.5)
            self.timeToLive -= 1
            if self.timeToLive == 0:
                self.alive = False
                netModule.onPlayerDisconnect(self.ID)
                self.connection.close()
                serverThread.removeClient(client)
                print(str(client.address) + " hatte ein Timeout und wurde gekickt.")
                print("Verbundene Clients: " + str(netModule.getPlayerCount()))
                break


    def refreshTTL(self):
        self.timeToLive = 3



class KEYPRESS(Enum):
    type = "KEYPRESS"

    LEFT = "LEFT_DOWN"
    RIGHT = "RIGHT_DOWN"
    UP = "UP_DOWN"
    DOWN = "DOWN_DOWN"
    SPACE = "SPACE_DOWN"

class KEYRELEASE(Enum):
    type = "KEYUP"

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


class NetModule():

    def getCmdQueue(self):
        return serverThread.getCmdQueue()

    def getPlayerCount(self):
        return len(serverThread.clientList)

    def sendGamestate(self, Gamestate):
        serverThread.sendToAll(Gamestate)

    def onKeyPress(self, PLAYERCOMMAND):
        print(PLAYERCOMMAND.ID + " hat eine Taste gedrückt: " + str(PLAYERCOMMAND.KEYEVENT))
        #
        if PLAYERCOMMAND.KEYEVENT == KEYPRESS.SPACE:
            player.jumping = True

        #
        pass

    def onKeyRelease(self, PLAYERCOMMAND):
        print(PLAYERCOMMAND.ID + " hat eine Taste losgelassen: " + str(PLAYERCOMMAND.KEYEVENT))
        #
        #
        #
        pass

    def onPlayerConnect(self, ID):
        #print(ID + " hat das Spiel betreten")
        pass

    def onPlayerDisconnect(self, ID):
        #print(ID + " hat das Spiel verlassen")
        pass


##############################################################
################  KLASSENLOSER CODE ADAM  ####################
##############################################################
serverThread = ThreadedServer()
serverThread.start()
netModule = NetModule()


import pygame
from pygame.locals import *


class Player(object):
    def __init__(self, rec_x, rec_y, direction):
        self.rec_x = rec_x
        self.rec_y = rec_y
        self.black = (0, 0, 0)
        self.blue = (0, 0, 255)
        self.red = (255, 0, 0)
        self.recSize = 60
        self.backSize = self.recSize * 0.1
        self.direction = direction
        self.rect = pygame.draw.rect(screen, self.black, (self.rec_x, self.rec_y, self.recSize, self.recSize))
        # self.weapon = pygame.draw.rect(screen, self.blue, (self.rec_x + self.recSize/2, self.rec_y + self.recSize/2,
        #                                                    10, 10))
        self.back_r = pygame.draw.rect(screen, self.red, (self.rec_x, self.rec_y, self.backSize, self.recSize))
        self.back_l = pygame.draw.rect(screen, self.red,
                                       (self.rec_x + self.recSize * 0.9, self.rec_y, self.backSize, self.recSize))
        self.speed = 10
        self.jump_height = 150
        self.jumping = False
        self.jump_offset = 0
        self.velocity_index = 0
        self.key_down = False

        self.velocity = list([(i / 2.0) - 7.5 for i in range(0, 31)])
        self.platform = 460


    def handle_keys(self):

        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                exit()
            elif e.type == KEYPRESS:
                key = e.key
                if key == K_LEFT:
                    self.direction = -1
                elif key == K_RIGHT:
                    self.direction = 1

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            self.run(-1, 0)
        elif pressed[pygame.K_RIGHT]:
            self.run(1, 0)

        elif pressed[K_UP]:
            self.jumping = True

        elif pressed[K_DOWN]:
            self.jumping = False

    def run(self, direction_x, direction_y):
        self.black = (0, 0, 0)
        screen.fill(white)
        screen.fill(green, rect=[0, 400 + player.recSize, screenWidth, 400 - player.recSize])
        screen.fill(black, rect=[0, 0, screenWidth, 100])
        # self.rect = self.rect.move(x * self.speed, y * self.speed)
        self.rect.move_ip(self.speed * direction_x, self.speed * direction_y)
        pygame.draw.rect(screen, self.black, self.rect)

        if self.direction == 1:
            self.back_r.move_ip(self.speed * direction_x, self.speed * direction_y)
            pygame.draw.rect(screen, self.red, self.back_r)
        else:
            self.back_l.move_ip(self.speed * direction_x, self.speed * direction_y)
            pygame.draw.rect(screen, self.red, self.back_l)

        if self.rect.left > screenWidth + self.recSize:
            self.rect.left = -self.recSize
        if self.rect.left < -self.recSize:
            self.rect.left = screenWidth + self.recSize

        if self.direction == 1:
            if self.back_r.left > screenWidth + self.recSize:
                self.back_r.left = -self.recSize
            if self.back_r.left < -self.recSize:
                self.back_r.left = screenWidth + self.recSize
        else:
            if self.back_l.left > screenWidth + self.recSize:
                self.back_l.left = -self.recSize
            if self.back_l.left < -self.recSize:
                self.back_l.left = screenWidth + self.recSize

    def draw(self, surface):
        pygame.draw.rect(screen, self.black, self.rect)
        # pygame.draw.rect(screen, self.black, self.weapon)
        if self.direction == 1:
            pygame.draw.rect(screen, self.red, self.back_r)
        else:
            pygame.draw.rect(screen, self.red, self.back_l)

    def jump(self, direction_x, direction_y):

        if self.jumping:
            self.jump_offset = self.velocity[self.velocity_index] * -4
            self.velocity_index += 1

            if self.rect.top == self.jump_height:
                self.jumping = False

            elif self.velocity_index >= len(self.velocity) - 1:
                self.velocity_index = len(self.velocity) - 1

            if self.jump_offset != 0 and self.rect.bottom > self.platform:
                self.jumping = False
                self.velocity_index = 0
                self.jump_offset = 0
                self.rect.bottom = self.platform

                if self.direction == 1:
                    self.back_r.bottom = self.platform
                else:
                    self.back_l.bottom = self.platform

        # if self.jumping:
        #     self.jump_offset = 5
        #     if self.rect.top == self.jump_height:
        #         self.jumping = False
        #
        # elif self.jump_offset > 0 and self.jumping is False:
        #     self.jump_offset = -5
        #
        # elif self.jump_offset != 0 and self.rect.bottom == self.platform:
        #     self.jump_offset = 0

        self.black = (0, 0, 0)
        screen.fill(white)
        screen.fill(green, rect=[0, 400 + self.recSize, screenWidth, 400 - self.recSize])
        screen.fill(black, rect=[0, 0, screenWidth, 150])
        self.rect.move_ip(direction_x * self.speed, direction_y * self.jump_offset)
        pygame.draw.rect(screen, self.black, self.rect)

        if self.direction == 1:
            self.back_r.move_ip(direction_x * self.speed, direction_y * self.jump_offset)
            pygame.draw.rect(screen, self.red, self.back_r)
        else:
            self.back_l.move_ip(direction_x * self.speed, direction_y * self.jump_offset)
            pygame.draw.rect(screen, self.red, self.back_l)


##############################################################
################  KLASSENLOSER CODE CARO ####################
##############################################################

screenWidth = 1200
screenHeight = 600
white = (255, 255, 255)
green = (0, 255, 0)
black = (0, 0, 0)
fps = 60

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Double Crossing")

pygame.init()

player = Player(10, 400, 1)
clock = pygame.time.Clock()
screen.fill(white)
screen.fill(green, rect=[0, 400 + player.recSize, screenWidth, 400 - player.recSize])
screen.fill(black, rect=[0, 0, screenWidth, 150])
player.draw(screen)
pygame.display.update()

def gameLoop():
    while True:
        netModule.sendGamestate( str(player.rect.left) + "," + str(player.rect.top) )
        player.handle_keys()
        player.jump(0, -1)
        pygame.display.update()
        clock.tick(fps)


        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                exit()

gameLoopThread = threading.Thread(target=gameLoop())
