import pygame
from utils import load_config
from snake import Snake
from food import Food

def main():
    config = load_config("config.json")
    board_size = config["board_size"]
    cell_size = config["cell_size"]
    obstacles = [tuple(obs) for obs in config["obstacles"]]

    # Inițializare pygame
    pygame.init()
    screen = pygame.display.set_mode(
        (board_size[0] * cell_size, board_size[1] * cell_size)
    )
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 20)

    # Inițializare joc
    snake = Snake((board_size[0] // 2, board_size[1] // 2))
    food = Food(board_size, obstacles, snake.body)
    score = 0
    high_score = 0

    # Bucla principală a jocului
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Controlul șarpelui (adaugă aici)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and snake.direction != (0, 1):  # Evităm să mergem direct în jos
            snake.direction = (0, -1)
        elif keys[pygame.K_DOWN] and snake.direction != (0, -1):  # Evităm să mergem direct în sus
            snake.direction = (0, 1)
        elif keys[pygame.K_LEFT] and snake.direction != (1, 0):  # Evităm să mergem direct la dreapta
            snake.direction = (-1, 0)
        elif keys[pygame.K_RIGHT] and snake.direction != (-1, 0):  # Evităm să mergem direct la stânga
            snake.direction = (1, 0)

        # Mișcarea șarpelui
        snake.move()

        # Verificare coliziune cu mâncarea
        if snake.body[0] == food.position:
            snake.grow()
            score += 1
            food = Food(board_size, obstacles, snake.body)

        # Verificare coliziuni
        if snake.check_collision(obstacles):
            high_score = max(high_score, score)
            print(f"Game Over! Score: {score}, High Score: {high_score}")
            running = False

        # Randare
        screen.fill((0, 0, 0))  # Fundal negru
        for x, y in snake.body:
            pygame.draw.rect(screen, (0, 255, 0), (x * cell_size, y * cell_size, cell_size, cell_size))
        pygame.draw.rect(screen, (255, 0, 0), (food.position[0] * cell_size, food.position[1] * cell_size, cell_size, cell_size))
        for x, y in obstacles:
            pygame.draw.rect(screen, (128, 128, 128), (x * cell_size, y * cell_size, cell_size, cell_size))

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()
