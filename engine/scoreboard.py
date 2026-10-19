from pathlib import Path
import pygame


class Scoreboard:
    def __init__(self, sprites, position=(16, 16), size=(120, 35), font=None, font_size=11):
        self.sprites = sprites
        self.position = position
        self.size = size
        self.font = font or self._load_default_font(font_size)
        self.background = self.sprites.get("scoreboard", size=self.size) if self.sprites.has_asset("scoreboard") else None
        if self.background is not None:
            self.background.set_alpha(160)
        self.rect = self.background.get_rect(topleft=self.position) if self.background else pygame.Rect(*self.position, *self.size)
        self.text_surf = None
        self.text_rect = None
        self.update(0)

    def _load_default_font(self, size: int) -> pygame.font.Font:
        font_file = Path(__file__).parent.parent / "assets" / "fonts" / "PressStart2P.ttf"
        if font_file.exists():
            try:
                return pygame.font.Font(str(font_file), size)
            except Exception:
                pass
        return pygame.font.SysFont("Arial", size)

    def update(self, score):
        self.text_surf = self.font.render(f"Score: {score}", True, "black")
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, surface):
        if self.background is not None:
            surface.blit(self.background, self.rect)
        if self.text_surf is not None:
            surface.blit(self.text_surf, self.text_rect)
