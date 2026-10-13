from logic.manager import manager
from engine.artist import artist
from engine.handleInput import HandleInputPygame
import pygame
import argparse
from collections import deque

WIDTH, HEIGHT = 80, 40
SCALE = 16
DIMENSIONS = (WIDTH, HEIGHT)
SNAKE_INFO = {
    # SKINS: default, default-2, demon
    "player1": {"size": 8, "skin": "default", "starting_pos": (40, 20)},
    "player2": {"size": 8, "skin": "default-2", "starting_pos": (60, 30)},
}
OBSTACLE_INFO = {"number": 15, "size_range": (3, 15)}

parser = argparse.ArgumentParser()
parser.add_argument("-2p", dest="two_player", action="store_true", help="Enable two player mode")
args=parser.parse_args()
frame_buffer = deque(maxlen=30)

game = manager(DIMENSIONS, SNAKE_INFO, OBSTACLE_INFO, player_count=2 if args.two_player else 1)
clock = pygame.time.Clock()
artist = artist(WIDTH, HEIGHT, SCALE)
input_handler = HandleInputPygame(game)
game.register(game.SCORE_CHANGED, artist.on_score_changed)
input_handler2 = None
if args.two_player:
    input_handler2 = HandleInputPygame(
        game,
        player=2,
        commands={"up": pygame.K_UP, "down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT},
    )

def check_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.stop()
        elif event.type == pygame.KEYDOWN:
            input_handler.handleInput(event.key)
            if input_handler2 is not None:
                input_handler2.handleInput(event.key)

def play_countdown(ticks):
    for i in range(ticks, 0, -1):
        artist.draw_map()
        artist.draw_obstacle(game.get_obstacles())
        artist.draw_food(game.get_food())
        for player in range(1, game.get_player_count() + 1):
            for segment in game.get_snake_segments(player):
                artist.draw_snake(segment)

        artist.update_countdown(i)
        artist.update()
        clock.tick(1)

def playback():
    for frame in frame_buffer:
        artist.blit_display(artist.vintage_playback_frame(frame), (0, 0), update=True)
        clock.tick(15)

def await_close():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    return
    
def run():
    play_countdown(3)
    while game.is_running():
        artist.draw_map()
        artist.draw_obstacle(game.get_obstacles())
        check_event()
        artist.draw_food(game.get_food())

        for player in range(1, game.get_player_count() + 1):
            for segment in game.get_snake_segments(player):
                artist.draw_snake(segment)

        artist.draw_score()

        # move snake
        message = game.update_snake()
        if message is not None:
            print(message)

        # update window
        frame_buffer.append(artist.copy_display())
        artist.update()
        clock.tick(15)

    playback()
    artist.game_over(game.death_reason, game.get_score())
    await_close()
    pygame.quit()

if __name__ == "__main__":
    run()