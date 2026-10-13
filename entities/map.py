from entities.snake.snake import snake
from entities.food import food
from entities.obstacle import obstacles
import random

class map:
    def __init__(self, dimensions, snake_info, obstacle_info, player_count=1, background_image=None):
        self.width, self.height = dimensions
        self.background_image = "default" if background_image is None else background_image
        self.snakes = [self.create_snake(snake_info["player1"], "default")]
        if player_count == 2:
            self.snakes.append(self.create_snake(snake_info["player2"], "default-2", (-1, 0)))

        self.obstacles = obstacles(
            obstacle_info["number"], 
            obstacle_info["size_range"],
            dimensions,
            self.get_protected_positions(),
        )
        self.food = food(self.get_free_position())

    def create_snake(self, snake_info, skin, direction=(1,0)):
        return snake(
            snake_info["size"],
            snake_info["starting_pos"],
            snake_info["skin"] if snake_info["skin"] else skin,
            direction
        )

    def get_snake(self, player=1):
        return self.snakes[player - 1]

    def get_snakes(self):
        return self.snakes

    def get_food(self):
        return self.food

    def get_obstacles(self):
        return self.obstacles

    def get_background(self):
        return self.background_image

    def get_protected_positions(self):
        protected_positions = self.get_snake_positions()
        for current_snake in self.snakes:
            head_x, head_y = current_snake.get_head_position()
            direction = current_snake.body[0].direction
            for distance in range(1, 10):
                protected_positions.append((
                    head_x + distance * direction[0],
                    head_y + distance * direction[1],
                ))
        return protected_positions

    def is_snake_on_obstacle(self, player=1):
        return self.obstacles.is_obstacle_at(self.get_snake(player).get_head_position())

    def is_snake_out_of_bounds(self, player=1):
        x, y = self.get_snake(player).get_head_position()
        return x not in range(self.width) or y not in range(self.height)

    def is_snake_on_snake(self, player):
        head_position = self.get_snake(player).get_head_position()
        for other_player, current_snake in enumerate(self.snakes, start=1):
            if other_player != player and head_position in self.get_snake_positions(other_player):
                return True
        return False

    def get_random_position(self):
        return (random.randint(0, self.width - 1), random.randint(0, self.height - 1))

    def get_free_position(self):
        while True:
            position = self.get_random_position()
            if not self.obstacles.is_obstacle_at(position) and position not in self.get_snake_positions():
                break
        return position

    def get_snake_positions(self, player=None):
        snakes = self.snakes if player is None else [self.get_snake(player)]
        return [
            segment.get_position()
            for current_snake in snakes
            for segment in current_snake.body
        ]

    def get_snake_segments(self, player=None):
        snakes = self.snakes if player is None else [self.get_snake(player)]
        return [
            segment
            for current_snake in snakes
            for segment in current_snake.body
        ]