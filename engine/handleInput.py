from logic.command import Command, InputHandler
import pygame

class UpPygame(Command):
    def execute(self, command):
        command.handleInput("w")

class DownPygame(Command):
    def execute(self, command):
        command.handleInput("s")

class LeftPygame(Command):
    def execute(self, command):
        command.handleInput("a")

class RightPygame(Command):
    def execute(self, command):
        command.handleInput("d")

class HandleInputPygame(InputHandler):
    def __init__(self, game, player=1, commands=None):
        if commands is None:
            commands = {"up": pygame.K_w, "down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d}
        self.command = {
            commands["up"]: UpPygame,
            commands["down"]: DownPygame,
            commands["left"]: LeftPygame,
            commands["right"]: RightPygame,
        }
        self.commandHandler = InputHandler(game, player)

    def handleInput(self, key):
        if key in self.command:
            self.command[key]().execute(self.commandHandler)