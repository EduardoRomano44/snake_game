from pathlib import Path

import pygame


SpriteDefinitions = dict[str, dict[str, Path]]

DEFAULT_SPRITES: SpriteDefinitions = {
    "snake_head": {
        "default": Path("assets") / "snake" / "default" / "snake-head.png",
        "default-2": Path("assets") / "snake" / "default-2" / "snake-head-2.png",
        "demon": Path("assets") / "snake" / "demon" / "snake-head.png",
    },
    "snake_body": {
        "default": Path("assets") / "snake" / "default" / "snake-body.png",
        "default-2": Path("assets") / "snake" / "default-2" / "snake-body-2.png",
        "demon": Path("assets") / "snake" / "demon" / "snake-body.png",   
    },
    "snake_body-cross": {
        "default": Path("assets") / "snake" / "default" / "snake-body-cross.png",
        "default-2": Path("assets") / "snake" / "default-2" / "snake-body-cross-2.png",
        "demon": Path("assets") / "snake" / "demon" / "snake-body-cross.png",
    },
    "food": {
        "default": Path("assets") / "food" / "basic-food.png",
    },
    "wall": {
        "default": Path("assets") / "wall" / "wall.png",
    },
    "background": {
        "default": Path("assets") / "others" / "background.png",
    },
    "scoreboard": {
        "default": Path("assets") / "others" / "scoreboard.png",
    },
}


class SpriteLibrary:
    """Loads, scales, and caches sprites by logical name and variant."""

    def __init__(self, cell_size, project_root=None, definitions=None):
        self.cell_size = cell_size
        self.project_root = project_root or Path(__file__).parent.parent
        self.definitions = DEFAULT_SPRITES if definitions is None else definitions
        self._cache = {}

    def get_asset_path(self, name, variant):
        variants = self.definitions.get(name)
        if variants is None:
            raise KeyError(f"Unknown sprite: {name}")

        asset_path = variants.get(variant)
        if asset_path is None:
            raise KeyError(f"Unknown variant '{variant}' for sprite '{name}'")

        return asset_path

    def has_asset(self, name, variant="default"):
        variants = self.definitions.get(name)
        return variants is not None and variant in variants

    def get(self, name, variant="default", rotation=0, size=(0, 0)):
        if size == (0, 0):
            size = (self.cell_size, self.cell_size)
        rotation %= 360
        cache_key = (name, variant, rotation, size)
        if cache_key in self._cache:
            return self._cache[cache_key]

        asset_path = self.get_asset_path(name, variant)
        raw = pygame.image.load(self.project_root / asset_path)
        try:
            image = raw.convert_alpha()
        except pygame.error:
            image = raw
        image = pygame.transform.scale(image, size)
        image = pygame.transform.rotate(image, rotation)
        self._cache[cache_key] = image
        return image

