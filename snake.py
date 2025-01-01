import pygame


class Snake:
    def __init__(self, initial_position):
        """
        Initialize the snake with the initial position.
        """
        self.body = [initial_position]
        self.direction = pygame.K_RIGHT

    def move(self, direction):
        """
        Move the snake in the given direction, using the arrow keys.
        """
        if direction == pygame.K_UP and self.direction != pygame.K_DOWN:
            self.direction = direction
        elif direction == pygame.K_DOWN and self.direction != pygame.K_UP:
            self.direction = direction
        elif direction == pygame.K_LEFT and self.direction != pygame.K_RIGHT:
            self.direction = direction
        elif direction == pygame.K_RIGHT and self.direction != pygame.K_LEFT:
            self.direction = direction

        head_x, head_y = self.body[0]
        if self.direction == pygame.K_UP:
            new_head = (head_x, head_y - 1)
        elif self.direction == pygame.K_DOWN:
            new_head = (head_x, head_y + 1)
        elif self.direction == pygame.K_LEFT:
            new_head = (head_x - 1, head_y)
        elif self.direction == pygame.K_RIGHT:
            new_head = (head_x + 1, head_y)

        self.body = [new_head] + self.body[:-1]

    def grow(self):
        """
        Add a new part to the snake's body.
        """
        tail = self.body[-1]
        if self.direction == pygame.K_UP:
            new_part = (tail[0], tail[1] + 1)
        elif self.direction == pygame.K_DOWN:
            new_part = (tail[0], tail[1] - 1)
        elif self.direction == pygame.K_LEFT:
            new_part = (tail[0] + 1, tail[1])
        elif self.direction == pygame.K_RIGHT:
            new_part = (tail[0] - 1, tail[1])
        self.body.append(new_part)

    def check_collision(self, obstacles, board_size):
        """
        Check if the snake has collided with itself, with the walls
        or with the obstacles.
        """
        head = self.body[0]
        if head in self.body[1:]:
            return True
        if head in obstacles:
            return True
        if (head[0] < 0 or head[0] >= board_size[0] or
                head[1] < 0 or head[1] >= board_size[1]):
            return True
        return False
