from entities.map import map
from logic.observer import Subject

class manager(Subject):
    SCORE_CHANGED = "score_changed"
    GAME_OVER = "game_over"

    def __init__(self, dim, snake_info=None, obstacle_info=None, player_count=1, background_image=None):
        super().__init__()
        if snake_info is None:
            snake_info = {"player1": {"size": 3, "color": "red", "starting_pos": (40, 20)}}
        if obstacle_info is None:
            obstacle_info = {"number": 5, "size_range": (2, 7)}

        self.map = map(dim, snake_info, obstacle_info, player_count, background_image)
        self.player_count = player_count
        self.score = 0
        self.running = True
        self.death_reason = None

    def stop(self):
        self.running = False

    def finish(self, reason):
        self.death_reason = reason
        self.running = False
        self.notify(self.GAME_OVER, self)

    def change_snake_direction(self, direction, player=1):
        self.map.get_snake(player).change_direction(direction)

    def is_running(self):
        return self.running

    def get_snake_color(self, player=1):
        return self.map.get_snake(player).get_color()
    
    def get_score(self):
        return self.score

    def get_background(self):
        return self.map.get_background()

    def get_food(self):
        return self.map.get_food()

    def get_obstacles(self):
        return self.map.get_obstacles()

    def get_snake_positions(self):
        return self.map.get_snake_positions()

    def get_snake_segments(self, player=1):
        return self.map.get_snake_segments(player)

    def get_player_count(self):
        return self.player_count

    def update_snake(self):
        snakes = self.map.get_snakes()
        food = self.map.get_food()
        for player, current_snake in enumerate(snakes, start=1):
            current_snake.update()
            death_reason = current_snake.is_dead()
            if death_reason is None and self.map.is_snake_out_of_bounds(player):
                death_reason = "Snake crashed against the wall"
            if death_reason is None and self.map.is_snake_on_obstacle(player):
                death_reason = "Snake crashed against an obstacle"
            if death_reason is None and self.map.is_snake_on_snake(player):
                death_reason = "Snake crashed against another player"
            if death_reason is not None:
                death_reason = f"Player {player}: {death_reason}"
                self.finish(death_reason)
                return death_reason

            if current_snake.try_eating(food.get_position()):
                self.score += 1
                self.map.get_food().set_position(self.map.get_free_position())
                self.notify(self.SCORE_CHANGED, self)
        return None