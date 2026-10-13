class Segment:
    def __init__(self, position, direction, sprite):
        self.position = position
        self.direction = direction
        self.sprite = sprite
        self.turn_rotation = None

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position

    def set_direction(self, direction):
        self.direction = direction

    def get_sprite(self):
        return self.sprite

    def set_sprite(self, sprite):
        self.sprite = sprite

    def set_turn_rotation(self, rotation):
        self.turn_rotation = rotation