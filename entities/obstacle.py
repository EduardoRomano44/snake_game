import random

class obstacle:
    def __init__(self, data):
        self.size = data["size"]
        self.direction = data["direction"]
        self.create_segments(data["starting_pos"], data["direction"])

    def create_segments(self, starting_pos, direction):
        self.segments = []
        for i in range(self.size):
            self.segments.append((starting_pos[0] + i * direction[0], starting_pos[1] + i * direction[1]))

    def get_segments(self):
        return self.segments

    def get_direction(self):
        return self.direction

class obstacles:
    def __init__(self, n, size_range, dimensions, forbidden_positions=None):
        if forbidden_positions is None:
            forbidden_positions = []
        self.obstacles = self.map_obstacles(n, size_range, dimensions, forbidden_positions)

    def map_obstacles(self, n, size_range, dimensions, forbidden_positions):
        obstacles = []
        for i in range(n):
            while True:
                size = random.randint(size_range[0], size_range[1])
                starting_pos = (random.randint(0, dimensions[0] - size), random.randint(0, dimensions[1] - size))
                direction = random.choice([(1, 0), (0, 1)])
                obstacle_data = {"size": size, "starting_pos": starting_pos, "direction": direction}
                candidate = obstacle(obstacle_data)
                if not any(position in forbidden_positions for position in candidate.get_segments()):
                    obstacles.append(candidate)
                    break
        return obstacles
    
    def is_obstacle_at(self, position):
        for obstacle in self.obstacles:
            if position in obstacle.get_segments():
                return True
        return False

    def get_obstacles(self):
        return self.obstacles
