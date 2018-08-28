import random
import threading
import sys
import os
import socket
import time
import traceback
import ws4py.framing
from enum import Enum
import uuid
from base64 import b64encode
from hashlib import sha1



class ThreadedServer(threading.Thread):

    IPFile = open("IP.txt", 'r')


    IP = IPFile.readline()[:-1]
    port = int(IPFile.readline())

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
        self.serverOn = True

    def run(self):
        self.serverLoop()

    def removeClient(self, client):
        self.clientList.remove(client)

    def serverLoop(self):

        while serverThread.serverOn:
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
            except Exception as e:
                traceback.print_exc()



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
        #############DIESE FUNKTION IST COPYPASTA

        opcode_and_fin = frame[0]

        payload_len = frame[1] - 128

        mask = frame[2:6]
        encrypted_payload = frame[6: 6 + payload_len]

        payload = bytearray([encrypted_payload[i] ^ mask[i % 4] for i in range(payload_len)])

        return payload

    def sendMsg(self, msg):
        f = ws4py.framing.Frame(opcode=0x1, body=msg, masking_key=None, fin=1, rsv1=0, rsv2=0, rsv3=0)
        try:
            self.connection.sendall( f.build() )
        except:
            print(str(self.connection) + " konnte nicht erreicht werden." )

    def inputLoop(self, client):
        while self.alive:
            try:
                frame = self.connection.recv(1024)
                msg = self.decodeFrame(frame).decode()
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

    def sendGameState(self):

        output = "["

        for player in playerList:

            output += "{"
            output += "\"ID\":" + str("\"" + player.ID + "\"") + ","
            output += "\"name\":" + "\"" + player.name + "\"" + ","
            output += "\"xPos\":" + str(player.rect.left) + ","
            output += "\"yPos\":" + str(player.rect.top) + ","
            output += "\"direction\":" + str(player.direction) + ","
            output += "\"speed\":" + str(player.speed) + ","
            output += "\"weaponLength\":" + str(player.weapon_length) + ","
            output += "\"attacking\":" + "\"" + str(player.hit) + "\"" + ","
            output += "\"kissing\":" + "\"" + str(player.kissing) + "\"" + ","
            output += "\"jumping\":" + "\"" + str(player.jumping) + "\"" + ","
            output += "\"yourID\":" + "\"" + self.ID + "\""
            output += "}"



            if playerList.index(player) < len(playerList) - 1:

                output += ","
            else:

                output += "]"

        self.sendMsg(bytes(output, 'utf-8'))


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
        # print(PLAYERCOMMAND.ID + " hat eine Taste gedrückt: " + str(PLAYERCOMMAND.KEYEVENT))
        #
        for player in playerList:
            if PLAYERCOMMAND.ID == player.ID:
                if PLAYERCOMMAND.KEYEVENT == KEYPRESS.UP:
                    player.jumping = True

                if PLAYERCOMMAND.KEYEVENT == KEYPRESS.DOWN:
                    player.jumping = False

                if PLAYERCOMMAND.KEYEVENT == KEYPRESS.RIGHT:
                    player.right = True

                if PLAYERCOMMAND.KEYEVENT == KEYPRESS.LEFT:
                    player.left = True

                if PLAYERCOMMAND.KEYEVENT == KEYPRESS.SPACE:
                    if not player.kissing:
                        player.hit = True
        pass

    def onKeyRelease(self, PLAYERCOMMAND):
        # print(PLAYERCOMMAND.ID + " hat eine Taste losgelassen: " + str(PLAYERCOMMAND.KEYEVENT))

        for player in playerList:
            if PLAYERCOMMAND.ID == player.ID:

                if PLAYERCOMMAND.KEYEVENT == KEYRELEASE.RIGHT:
                    player.right = False
                    player.speed = 2

                if PLAYERCOMMAND.KEYEVENT == KEYRELEASE.LEFT:
                    player.left = False
                    player.speed = 2

                if PLAYERCOMMAND.KEYEVENT == KEYRELEASE.SPACE:
                    player.hit = False

        #
        #
        pass

    def onPlayerConnect(self, ID):
        # print(ID + " hat das Spiel betreten")

        playerList.append(Player(ID))

        pass

    def onPlayerDisconnect(self, ID):
        # print(ID + " hat das Spiel verlassen")
        for player in playerList:
            if ID == player.ID:
                playerList.remove(player)

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

    def __init__(self, ID):
        self.ID = ID
        self.name = "Max Mustermann"
        self.recSize = 45
        self.weapon_length = 100
        self.rec_x = random.randint(0+ (self.recSize + self.weapon_length),
                                    screenWidth - (self.recSize + self.weapon_length))
        self.rec_y = 400
        self.black = (0, 0, 0)
        self.blue = (0, 0, 255)
        self.red = (255, 0, 0)
        self.backSize = self.recSize * 0.1
        self.list_direction = [-1, 1]
        self.direction = random.choice(self.list_direction)
        self.rect = pygame.draw.rect(screen, self.black, (self.rec_x, self.rec_y, self.recSize, self.recSize))
        self.weapon_r = pygame.draw.rect(screen, self.blue, (self.rect.left + self.recSize / 2, self.rect.top +
                                                             self.recSize / 2, self.weapon_length, 10))
        self.weapon_l = pygame.draw.rect(screen, self.blue, (self.rect.left + self.recSize / 2, self.rect.top +
                                                             self.recSize / 2, -self.weapon_length, 10))
        self.speed = 3
        self.maxspeed = 13

        self.jump_speed = 0
        self.jump_height = 150
        self.jumping = False
        self.jump_offset = 0
        self.velocity_index = 0

        # self.velocity = list([(i / 2.0) - 7.5 for i in range(0, 31)])
        self.velocity_up = list([i for i in range(-24, 0)])
        self.velocity_down = list([i for i in range(2, 24)])
        self.platform = 445

        self.left = False
        self.right = False
        self.hit = False
        self.gravity = 5
        self.on_ground = True

        self.kissing = False

    def handle_keys(self):

        if self.left:
            self.direction = -1
            self.run(-1, 0)


        if self.right:
            self.direction = 1
            self.run(1, 0)

    def run(self, direction_x, direction_y):
        self.black = (0, 0, 0)

        self.rect.move_ip(self.speed * direction_x, self.gravity * direction_y)

        if self.speed < self.maxspeed:
            self.speed += 0.1

        if self.direction == 1:
            self.weapon_r.left = self.rect.left + self.recSize / 2
            self.weapon_r.top = self.rect.top + self.recSize / 2
        elif self.direction == -1:
            self.weapon_l.right = self.rect.left + self.recSize / 2
            self.weapon_l.top = self.rect.top + self.recSize / 2

        if self.rect.left > screenWidth + self.recSize:
            self.rect.left = -self.recSize
        if self.rect.left < -self.recSize:
            self.rect.left = screenWidth + self.recSize

    def draw(self, surface):

        pygame.draw.rect(screen, self.black, self.rect)

        if self.direction == 1:
            pygame.draw.rect(screen, self.blue, self.weapon_r)
            self.weapon_r = pygame.draw.rect(screen, self.blue, (self.rect.left + self.recSize / 2, self.rect.top +
                                                             self.recSize / 2, self.weapon_length, 10))
        elif self.direction == -1:
            self.weapon_l = pygame.draw.rect(screen, self.blue, (self.rect.left + self.recSize / 2, self.rect.top +
                                                            self.recSize / 2, -self.weapon_length, 10))
            pygame.draw.rect(screen, self.blue, self.weapon_l)


    def jump(self, direction_x, direction_y):

        if self.rect.bottom >= self.platform:
            self.on_ground = True
        else:
            self.on_ground = False

        if self.jumping:
            self.jump_speed = self.velocity_up[self.velocity_index]
            self.velocity_index += 1

            if self.velocity_index >= len(self.velocity_up) - 1:
                self.velocity_index = len(self.velocity_up) - 1

        if  self.jump_speed == -2:
            self.jumping = False
            self.velocity_index = 0

        if self.jumping is False and self.jump_speed != 0:
            self.jump_speed = self.velocity_down[self.velocity_index]
            self.velocity_index += 1

            if self.velocity_index >= len(self.velocity_down) - 1:
                self.velocity_index = len(self.velocity_down) - 1

            if self.rect.bottom >= self.platform:
                self.jump_speed = 0
                self.rect.bottom = self.platform
                self.velocity_index = 0

        self.rect.move_ip(direction_x * self.speed, direction_y * self.jump_speed)

        if self.direction == 1:
            self.weapon_r.top = self.rect.top + self.recSize / 2
        elif self.direction == -1:
            self.weapon_l.top = self.rect.top + self.recSize / 2

    def attacked(self):
        self.weapon_length += 10
        self.maxspeed *= 0.9


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

playerList = []

clock = pygame.time.Clock()

pygame.display.update()

def hitdetection():
    for attackingPlayer in playerList:
        for attackedPlayer in playerList:

            if attackingPlayer.hit is True and abs(attackingPlayer.rect.top - attackedPlayer.rect.top) < 15:
                if attackingPlayer.direction == attackedPlayer.direction:
                    if attackingPlayer.rect.left * attackingPlayer.direction < attackedPlayer.rect.left * attackedPlayer.direction:
                         if abs(attackingPlayer.rect.left - attackedPlayer.rect.left) < attackingPlayer.weapon_length:
                             playerList.remove(attackedPlayer)
                             attackingPlayer.attacked()


def collision():
    for player1 in playerList:
        for player2 in playerList:

            # if player1.hit is True:
            #     if (player1.weapon_length + player1.recSize/2) >= abs(player1.rect.left - player2.rect.left) \
            #             and player1 != player2 and player1.rect.bottom == player2.rect.bottom \
            #             and player1.direction == player2.direction:
            #         playerList.remove(player2)
            #         player1.attacked()

            if pygame.sprite.collide_rect(player1, player2) and player1 != player2 \
                and player1.rect.bottom == player2.rect.bottom:
                #print("colliding")

                while(player1.rect.left < player2.rect.left and player1.rect.left + player1.recSize > player2.rect.left):
                    player1.rect.left -= 1
                    player2.rect.left +=1

                # while (player1.rect.left > player2.rect.left):
                #     player1.rect.left -= 1
                #     player2.rect.left += 1

                # if player1.rect.left < player2.rect.left:
                #     player1.rect.right = player2.rect.left
                #
                # if player1.rect.left > player2.rect.left:
                #     player1.rect.left = player2.rect.right
                #
                # if player1.rect.bottom <= (player2.rect.bottom - player2.recSize):
                #     player1.rect.bottom = (player2.rect.bottom - player2.recSize)


            if pygame.sprite.collide_rect(player1, player2) \
                    and player1 != player2 \
                    and player1.rect.top < player2.rect.top:
                player1.rect.top = player2.rect.top - player2.recSize - 1
                if player1.direction == 1:
                    player1.weapon_r.top = player1.rect.top + player1.recSize / 2
                elif player1.direction == -1:
                    player1.weapon_l.top = player1.rect.top + player1.recSize / 2

                if player1.jumping:
                    player1.velocity_index = 0

                if player1.jumping is False:
                    player1.velocity_index = 5

                if player1.jumping is False and player2.jumping:
                    player1.jumping = True

def kissing():

    for i in range(0, len(playerList)):
        for j in range(i+1, len(playerList)):

            player1 = playerList[i]
            player2 = playerList[j]

            if player1 != player2 and player1.direction != player2.direction and player1.rect.bottom == player2.rect.bottom and abs( player1.rect.left - player2.rect.left ) <= player1.recSize + 5:

               if player1.rect.left < player2.rect.left and player1.direction == 1 and player2.direction == -1:
                    player1.kissing = True
                    player2.kissing = True

               if player1.rect.left > player2.rect.left and player1.direction == -1 and player2.direction == 1:
                   player1.kissing = True
                   player2.kissing = True

            elif player1 != player2:
                player1.kissing = False
                player2.kissing = False


def gameLoop():

    while serverThread.serverOn:
        screen.fill(white)
        screen.fill(green, rect=[0, 400 + 45, screenWidth, 400 - 45])
        screen.fill(black, rect=[0, 0, screenWidth, 150])
        collision()
        hitdetection()
        kissing()

        for connection in serverThread.clientList:
            connection.sendGameState()

        for player in playerList:

            for player1 in playerList:
                for player2 in playerList:
                    if pygame.sprite.collide_rect(player1, player2) and player1 != player2:
                        player1.rec_x = random.randint(0 + (player1.recSize + player1.weapon_length),
                                                       screenWidth - (player1.recSize + player1.weapon_length))

                    player.draw(screen)

            player.handle_keys()

            player.jump(0, 1)

        pygame.display.update()
        #clock.tick_busy_loop(80)
        clock.tick(100)

        for e in pygame.event.get():
            if e.type == QUIT:
                serverThread.serverOn = False

                for client in serverThread.clientList:
                    client.alive = False

                pygame.quit()
                sys.exit(0)
                os._exit(0)
                exit(0)

                break

    gameLoopThread = threading.Thread(target=gameLoop())

gameLoopThread = threading.Thread(target=gameLoop())
