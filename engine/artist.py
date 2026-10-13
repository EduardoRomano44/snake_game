from pathlib import Path
import pygame
import random

from engine.sprite_library import SpriteLibrary
from engine.scoreboard import Scoreboard

class artist:
    def __init__(self, width, height, scale, font_name="PressStart2P", font_size=20, sprites=None, score_font_size=11):
        self.width = width
        self.height = height
        self.scale = scale
        self.display = pygame.display.set_mode((scale * width, scale * height))
        self.sprites = sprites or SpriteLibrary(scale)
        pygame.font.init()
        self.font_name = font_name
        self.font = self.get_font(font_size)
        self.scoreboard = Scoreboard(
            self.sprites,
            position=(self.scale, self.scale),
            size=(120, 35),
            font=self.get_font(score_font_size),
        )

    def get_font(self, size: int) -> pygame.font.Font:
        font_file = Path(__file__).parent.parent / "assets" / "fonts" / "PressStart2P.ttf"
        if font_file.exists():
            try:
                return pygame.font.Font(str(font_file), size)
            except Exception:
                pass
        return pygame.font.SysFont("Arial", size)

    def copy_display(self):
        return self.display.copy()

    def blit_display(self, image, position=(0,0), update=False):
        self.display.blit(image, position)
        if update:
            pygame.display.flip()

    def on_score_changed(self, context):
        self.scoreboard.update(context.get_score())

    def draw_score(self):    
        self.scoreboard.draw(self.display)

    def draw_map(self, variant="default"):
        if variant is None:
            self.display.fill("white")
            return

        if variant == "end":
            self.display.fill("black")
            return

        background_image = self.sprites.get("background", variant, size=self.display.get_size())
        self.display.blit(background_image, (0, 0))

    def draw_snake(self, segment):
        sprite = segment.get_sprite()
        rotations = {
            (1, 0): 0,
            (0, -1): 90,
            (-1, 0): 180,
            (0, 1): 270,
        }
        rotation = segment.turn_rotation
        if rotation is None:
            rotation = rotations[segment.direction]
        sprite_name = f"snake_{sprite.part}"
        if not self.sprites.has_asset(sprite_name, sprite.skin):
            sprite_name = "snake_body"
            rotation = rotations[segment.direction]

        image = self.sprites.get(
            sprite_name,
            sprite.skin,
            rotation=rotation,
        )
        position = segment.get_position()
        self.display.blit(
            image,
            (self.scale * position[0], self.scale * position[1]),
        )

    def draw_obstacle(self, obstacles, variant="default"):
        for obstacle in obstacles.get_obstacles():
            direction = obstacle.get_direction()
            rotation = 90 if direction == (0, 1) else 0
            wall_sprite = self.sprites.get("wall", variant, rotation)
            for position in obstacle.get_segments():
                self.display.blit(wall_sprite,(self.scale * position[0], self.scale * position[1]))

    def draw_food(self, food, variant="default"):
        position = food.get_position()
        self.display.blit(self.sprites.get("food", variant), (self.scale * position[0], self.scale * position[1]))
    
    def update(self):
        pygame.display.flip()

    def update_countdown(self, countdown):
        font_size = max(24, self.scale * 4)
        font = self.get_font(font_size)

        grayed_out = pygame.Surface(self.display.get_size(), pygame.SRCALPHA)
        grayed_out.fill((200, 200, 200, 150))
        self.display.blit(grayed_out, (0, 0))

        countdown_text = font.render(str(countdown), True, "black")
        countdown_rect = countdown_text.get_rect(
            center=(
                self.display.get_width() / 2,
                self.display.get_height() / 2
            )
        )
        self.display.blit(countdown_text, countdown_rect)

    def vintage_playback_frame(self, frame):
        #Made with copilot
        vintage_frame = frame.copy()
        vintage_frame.fill((255, 220, 170), special_flags=pygame.BLEND_RGB_MULT)

        overlay = pygame.Surface(vintage_frame.get_size(), pygame.SRCALPHA)
        overlay.fill((20, 10, 0, 45))
        vintage_frame.blit(overlay, (0, 0))

        static = pygame.Surface(vintage_frame.get_size(), pygame.SRCALPHA)
        static_width, static_height = static.get_size()
        for y in range(0, static_height, 3):
            color = random.choice([(255, 255, 255), (0, 0, 0)])
            alpha = random.randint(12, 42)
            pygame.draw.line(static, (*color, alpha), (0, y), (static_width, y))
        for _ in range(static_width * static_height // 1600):
            x = random.randrange(static_width)
            y = random.randrange(static_height)
            alpha = random.randint(20, 65)
            pygame.draw.rect(static, (255, 255, 255, alpha), (x, y, 2, 2))
        vintage_frame.blit(static, (0, 0))

        font = self.get_font(max(18, self.scale * 2))
        label = font.render("DEATH CAM", True, (0, 0, 0))
        label_rect = label.get_rect(center=(self.scale*(self.width - 15), 35))
        circle_radius = max(5, self.scale // 2)
        circle_center = (label_rect.left - circle_radius - 10, label_rect.centery)
        pygame.draw.circle(vintage_frame, (210, 25, 25), circle_center, circle_radius)
        vintage_frame.blit(label, label_rect)
        return vintage_frame
    
    def game_over(self, message, score):
        self.draw_map("end")
        messages = ["Game Over", message, f"Score: {score}", "Press Enter to exit"]
        color = ["red", "white", "white", "gray"]
        text_sizes = [40, 18, 22, 14]
        for i in range(len(messages)):
            font = self.get_font(text_sizes[i])
            text_render = font.render(messages[i], True, color[i])
            text_rect = text_render.get_rect(center=(self.width * self.scale / 2, self.height * self.scale / 2 + (i * 75) - 50))
            self.display.blit(text_render, text_rect)

        pygame.display.flip()