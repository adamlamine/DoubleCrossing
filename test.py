class Game:

    zahl = None
    player = None

    def __init__(self, zahl):
        self.zahl = zahl
        self.player = Player(self, 50)

class Player():

    zahl = None
    game = None

    def __init__(self, game, zahl):
        self.zahl = zahl
        self.game = game

game = Game(133)

print(game.zahl)
print (game.player.zahl)