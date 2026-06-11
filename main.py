from scren import Game as ScreenGame
from game import GameController


player_name = ScreenGame().run()

game = GameController(player_name)
game.run()