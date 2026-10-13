from logic.command import Command

class MoveSnakeCommand(Command):
    def __init__(self, snake, direction):
        self.snake = snake
        self.direction = direction
    def execute(self):
        self.snake.input.change_direction(self.direction)