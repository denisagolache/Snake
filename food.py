import random

class Food:
    def __init__(self, board_size, obstacles, snake_body):
        self.board_size = board_size
        self.position = self.generate_new_position(obstacles, snake_body)

    def generate_new_position(self, obstacles, snake_body):
        while True:
            x = random.randint(0, self.board_size[0] - 1)
            y = random.randint(0, self.board_size[1] - 1)
            if (x, y) not in obstacles and (x, y) not in snake_body:
                return (x, y)
