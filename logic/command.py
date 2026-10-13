import pygame

class Command:
    def __init__(self):
        pass
    
    def execute(self):
        pass

class UpCommand(Command):
    def execute(self, game, player=1):
        game.change_snake_direction("up", player)

class DownCommand(Command):
    def execute(self, game, player=1):
        game.change_snake_direction("down", player)

class LeftCommand(Command):
    def execute(self, game, player=1):
        game.change_snake_direction("left", player)

class RightCommand(Command):
    def execute(self, game, player=1):
        game.change_snake_direction("right", player)

class InputHandler:
    def __init__(self, game, player=1):
        self.command = {
            "w": UpCommand,
            "s": DownCommand,
            "a": LeftCommand,
            "d": RightCommand,
        }
        self.game = game
        self.player = player
    
    def handleInput(self, key):
        if key in self.command:
            self.command[key]().execute(self.game, self.player)
    