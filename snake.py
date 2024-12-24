import pygame

class Snake:
    def __init__(self, position):
        self.body = [position]
        self.direction = pygame.K_RIGHT

    def move(self, direction):
        if direction == pygame.K_UP and self.direction != pygame.K_DOWN:
            self.direction = pygame.K_UP
        elif direction == pygame.K_DOWN and self.direction != pygame.K_UP:
            self.direction = pygame.K_DOWN
        elif direction == pygame.K_LEFT and self.direction != pygame.K_RIGHT:
            self.direction = pygame.K_LEFT
        elif direction == pygame.K_RIGHT and self.direction != pygame.K_LEFT:
            self.direction = pygame.K_RIGHT

        head = self.body[0]
        if self.direction == pygame.K_UP:
            new_head = (head[0], head[1] - 1)
        elif self.direction == pygame.K_DOWN:
            new_head = (head[0], head[1] + 1)
        elif self.direction == pygame.K_LEFT:
            new_head = (head[0] - 1, head[1])
        elif self.direction == pygame.K_RIGHT:
            new_head = (head[0] + 1, head[1])

        self.body = [new_head] + self.body[:-1]

    def grow(self):
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
        head = self.body[0]
        if head in self.body[1:]:  
            return True
        if head in obstacles: 
            return True
        if head[0] < 0 or head[0] >= board_size[0] or head[1] < 0 or head[1] >= board_size[1]:  # Coliziune cu marginea
            return True
        return False
