from entities.entity import Entity
from entities.snake.snake_components import SnakeCollisionComponent, SnakeInputComponent, SnakeMovementComponent, SnakeRenderComponent

class snake(Entity):
    def __init__(self, size, starting_pos, skin="default", direction=(1, 0)):
        super().__init__()

        self.render = SnakeRenderComponent(skin)
        self.input = SnakeInputComponent(direction)
        self.movement = SnakeMovementComponent(
            starting_pos,
            size,
            direction,
            head_sprite=self.render.head_sprite,
            body_sprite=self.render.body_sprite,
        )
        self.collision = SnakeCollisionComponent()

        self.add_component(SnakeRenderComponent, self.render)
        self.add_component(SnakeInputComponent, self.input)
        self.add_component(SnakeMovementComponent, self.movement)
        self.add_component(SnakeCollisionComponent, self.collision)

    @property
    def size(self):
        return self.movement.size

    @size.setter
    def size(self, value):
        self.movement.size = value

    @property
    def body(self):
        return self.movement.body

    def change_direction(self, direction_name):
        self.input.change_direction(direction_name)

    def get_head_position(self):
        return self.movement.body[0].get_position() if self.movement.body else None

    def increase_size(self):
        self.movement.increase_size()

    def try_eating(self, food_position):
        return self.collision.try_eating(food_position)

    def is_dead(self):
        if self.collision.is_self_colliding():
            return "Snake eats self"
        return None

    def update(self):
        self.input.update()
        self.movement.update()
        self.collision.update()
        self.render.update()