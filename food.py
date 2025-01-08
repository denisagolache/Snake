import random


class Food:
    def __init__(self, board_size, obstacles, snake_body):
        """
        Initialize the food with a random position that is not
        on the snake's body or on an obstacle.
        """
        self.board_size = board_size
        self.obstacles = obstacles
        self.snake_body = snake_body
        self.position = self.generate_new_position(obstacles, snake_body)

    def generate_new_position(self, obstacles, snake_body, min_distance=2):
        """
        Generate a new position for the food that is not on
        the snake's body or on an obstacle.
        """
        while True:
            new_position = (random.randint(0, self.board_size[0] - 1), 
                            random.randint(0, self.board_size[1] - 1))

            if (
                new_position not in snake_body
                and all(self.calculate_distance(new_position, obs)
                        >= min_distance for obs in obstacles)
            ):
                return new_position

    def calculate_distance(self, pos1, pos2):
        """
        Calculate the Manhattan distance between two positions.
        """
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
