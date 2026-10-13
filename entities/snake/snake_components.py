from logic.component import Component
from entities.snake.segment import Segment
from entities.snake.snake_sprite import snake_sprite_factory

class SnakeInputComponent(Component):
    DIRECTIONS = {
        "up": (0, -1),
        "down": (0, 1),
        "left": (-1, 0),
        "right": (1, 0),
    }

    def __init__(self, initial_direction=(1, 0)):
        super().__init__()
        self.current_direction = initial_direction
        self.next_direction = initial_direction

    def change_direction(self, direction_name):
        if direction_name not in self.DIRECTIONS:
            return
        target = self.DIRECTIONS[direction_name]
        if (self.current_direction[0] + target[0], self.current_direction[1] + target[1]) == (0, 0):
            return
        self.next_direction = target

    def update(self):
        self.current_direction = self.next_direction


class SnakeMovementComponent(Component):
    def __init__(self, starting_pos, size, initial_direction=(1, 0), head_sprite=None, body_sprite=None):
        super().__init__()
        self.size = size
        self.direction = initial_direction
        self.head_sprite = head_sprite
        self.body_sprite = body_sprite
        self.body = []
        self._init_body(starting_pos, initial_direction)

    def _init_body(self, starting_pos, direction):
        self.body = [ Segment(starting_pos, direction, self.head_sprite) ]
        for i in range(1, self.size):
            self.body.append(
                Segment(
                    ( starting_pos[0] - i * direction[0], starting_pos[1] - i * direction[1]),
                    direction,
                    self.body_sprite,
                )
            )

    def increase_size(self):
        self.size += 1

    def update(self):
        input_comp = self.entity.get_component(SnakeInputComponent) if self.entity else None
        if input_comp:
            self.direction = input_comp.current_direction

        # Update head direction if direction changed
        if self.body and self.body[0].direction != self.direction:
            self.body[0].movement_direction = self.body[0].direction
            self.body[0].direction = self.direction

        previous_positions = [segment.get_position() for segment in self.body]
        previous_directions = [segment.direction for segment in self.body]

        head = self.body[0]
        head.set_direction(self.direction)
        head.set_position((
            head.position[0] + self.direction[0],
            head.position[1] + self.direction[1]
        ))

        for i in range(1, len(self.body)):
            self.body[i].set_position(previous_positions[i - 1])
            self.body[i].set_direction(previous_directions[i - 1])

        while len(self.body) > self.size:
            self.body.pop()
        
        render_comp = self.entity.get_component(SnakeRenderComponent) if self.entity else None
        body_sprite = render_comp.body_sprite if render_comp else self.body_sprite

        while len(self.body) < self.size:
            self.body.append(Segment(previous_positions[-1], previous_directions[-1], body_sprite))

class SnakeCollisionComponent(Component):
    def __init__(self):
        super().__init__()

    def is_self_colliding(self):
        movement = self.entity.get_component(SnakeMovementComponent) if self.entity else None
        if not movement or not movement.body:
            return False
        head_pos = movement.body[0].get_position()
        body_positions = [s.get_position() for s in movement.body]
        return body_positions.count(head_pos) > 1

    def try_eating(self, food_position):
        movement = self.entity.get_component(SnakeMovementComponent) if self.entity else None
        if not movement or not movement.body:
            return False
        if movement.body[0].get_position() == food_position:
            movement.increase_size()
            return True
        return False

    def update(self):
        pass


class SnakeRenderComponent(Component):
    TURN_ROTATIONS = {
        frozenset({(-1, 0), (0, -1)}): 0,
        frozenset({(0, -1), (1, 0)}): 270,
        frozenset({(1, 0), (0, 1)}): 180,
        frozenset({(0, 1), (-1, 0)}): 90,
    }

    def __init__(self, skin="default"):
        super().__init__()
        self.skin = skin
        self.head_sprite = snake_sprite_factory.get(skin, "head")
        self.body_sprite = snake_sprite_factory.get(skin, "body")
        self.body_cross_sprite = snake_sprite_factory.get(skin, "body-cross")

    def update(self):
        movement = self.entity.get_component(SnakeMovementComponent) if self.entity else None
        if not movement or not movement.body:
            return

        body = movement.body
        for index, current_segment in enumerate(body[1:-1], start=1):
            previous_segment = body[index - 1]
            next_segment = body[index + 1]
            directions = frozenset({
                    (previous_segment.position[0] - current_segment.position[0], previous_segment.position[1] - current_segment.position[1]),
                    (next_segment.position[0] - current_segment.position[0], next_segment.position[1] - current_segment.position[1]),
                })
            if directions in self.TURN_ROTATIONS:
                current_segment.set_sprite(self.body_cross_sprite)
                current_segment.set_turn_rotation(self.TURN_ROTATIONS[directions])
            else:
                current_segment.set_sprite(self.body_sprite)
                current_segment.set_turn_rotation(None)

        if len(body) > 1:
            last_segment = body[-1]
            previous_segment = body[-2]
            last_segment.set_direction((previous_segment.position[0] - last_segment.position[0],previous_segment.position[1] - last_segment.position[1]))
            last_segment.set_sprite(self.body_sprite)
            last_segment.set_turn_rotation(None)
