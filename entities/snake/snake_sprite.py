class snake_sprite:
    def __init__(self, skin, part):
        self.skin = skin
        self.part = part


class snake_sprite_factory:
    _sprites = {}

    @classmethod
    def get(cls, skin, part):
        key = (skin, part)
        if key not in cls._sprites:
            cls._sprites[key] = snake_sprite(skin, part)
        return cls._sprites[key]