import json
import pygame
import sys
import random
from utils import load_config
from snake import Snake
from food import Food

def load_config(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def draw_text(screen, text, font, color, position):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def show_welcome_screen(screen, font, board_size, cell_size):
    welcome_image = pygame.image.load("welcome_image.png")
    welcome_image = pygame.transform.scale(welcome_image, (board_size[0] * cell_size, board_size[1] * cell_size))
    screen.fill((0, 0, 0))
    screen.blit(welcome_image, (0, 0))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

def main():
    if len(sys.argv) < 2:
        print("Usage: python game.py <config_file>")
        sys.exit(1)

    pygame.init()
    cell_size = 20
    config = load_config(sys.argv[1])
    board_size = config["board_size"]
    obstacles = [tuple(obs) for obs in config["obstacles"]]

    screen = pygame.display.set_mode((board_size[0] * cell_size, board_size[1] * cell_size))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    high_score = 0

    show_welcome_screen(screen, font, board_size, cell_size)

    snake_segment_image = pygame.image.load("snake_segment.png")
    snake_segment_image = pygame.transform.scale(snake_segment_image,(int(cell_size * 1.7), int(cell_size * 1.7)))
    food_image = pygame.image.load("food.png")
    food_image = pygame.transform.scale(food_image, (int(cell_size * 1.7), int(cell_size * 1.7)))
    obstacle_image = pygame.image.load("stone.png")
    obstacle_image = pygame.transform.scale(obstacle_image, (int(cell_size * 2), int(cell_size * 2)))

    def start_game():
        nonlocal high_score
        snake = Snake((board_size[0] // 2, board_size[1] // 2))
        food = Food(board_size, obstacles, snake.body)
        score = 0
        speed = 5
        running = True
        direction = pygame.K_RIGHT

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                        direction = event.key

            snake.move(direction)

            if snake.body[0] == food.position:
                score += 1
                speed = min(15, speed + 0.5)
                food.position = food.generate_new_position(obstacles, snake.body)
                snake.grow()

            if snake.check_collision(obstacles, board_size):
                high_score = max(high_score, score)
                return score

            screen.fill((0, 0, 0))

            for x, y in snake.body:
                screen.blit(snake_segment_image, (x * cell_size, y * cell_size))

            screen.blit(food_image, (food.position[0] * cell_size, food.position[1] * cell_size))

            for x, y in obstacles:
                screen.blit(obstacle_image, (x * cell_size - cell_size // 2, y * cell_size - cell_size // 2))

            score_text = font.render(f"Score: {score}  High Score: {high_score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

            pygame.display.flip()
            clock.tick(speed)

    def show_game_over_screen(score):
        game_over_image = pygame.image.load("game_over_image.png")
        game_over_image = pygame.transform.scale(game_over_image, (board_size[0] * cell_size, board_size[1] * cell_size))
        screen.fill((0, 0, 0))
        screen.blit(game_over_image, (0, 0))
        draw_text(screen, f"Score: {score}", font, (255, 255, 255), (10, 10))
        draw_text(screen, f"High Score: {high_score}", font, (255, 255, 255), (10, 50))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    while True:
        score = start_game()
        show_game_over_screen(score)

if __name__ == "__main__":
    main()
