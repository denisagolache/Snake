import json
import pygame
import sys
import random
import time
import os
from utils import load_config
from snake import Snake
from food import Food


def draw_text(screen, text, font, color, position, shadow_color=None):
    if shadow_color:
        shadow_pos = (position[0] + 2, position[1] + 2)  
        text_surface_shadow = font.render(text, True, shadow_color)
        screen.blit(text_surface_shadow, shadow_pos)

    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)


def show_welcome_screen(screen, font, board_size, cell_size):
    welcome_image = pygame.image.load("welcome_image.png")
    welcome_image = pygame.transform.scale(
        welcome_image, (board_size[0] * cell_size, board_size[1] * cell_size)
    )
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
    config_file = sys.argv[1]
    config = load_config(config_file)
    board_size = config["board_size"]
    initial_obstacles = [tuple(obs) for obs in config["obstacles"]]

    screen = pygame.display.set_mode(
        (board_size[0] * cell_size, board_size[1] * cell_size)
    )
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    font = pygame.font.Font("OpenSans-VariableFont_wdth,wght.ttf", 36)
    shadow_color = (0, 0, 0)
    text_color = (255, 255, 255)

    high_score = 0

    show_welcome_screen(screen, font, board_size, cell_size)

    snake_segment_image = pygame.image.load("snake_segment.png")
    snake_segment_image = pygame.transform.scale(
        snake_segment_image, (int(cell_size * 2), int(cell_size * 2))
    )
    snake_head_image = pygame.image.load("snake_head.png")
    snake_head_image = pygame.transform.scale(
        snake_head_image, (int(cell_size * 2), int(cell_size * 2))
    )
    food_image = pygame.image.load("food.png")
    food_image = pygame.transform.scale(
        food_image, (int(cell_size * 2), int(cell_size * 2))
    )
    special_food_image = pygame.image.load("special_food.png")
    special_food_image = pygame.transform.scale(
        special_food_image, (int(cell_size * 2), int(cell_size * 2))
    )
    obstacle_image = pygame.image.load("stone.png")
    obstacle_image = pygame.transform.scale(
        obstacle_image, (int(cell_size * 2), int(cell_size * 2))
    )
    background_image = pygame.image.load("background.png")
    background_image = pygame.transform.scale(
        background_image, (board_size[0] * cell_size, board_size[1] * cell_size)
    )

    def start_game():
        nonlocal high_score
        snake = Snake((board_size[0] // 2, board_size[1] // 2))
        food = Food(board_size, initial_obstacles, snake.body)
        special_food = None
        special_food_timer = None
        score = 0
        speed = 5
        running = True
        obstacles = initial_obstacles.copy()

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
                food.position = food.generate_new_position(obstacles, snake.body)
                snake.grow()

                if score % 5 == 0 and score >= 5:
                    speed = min(15, speed + 1)
                    for _ in range(3):
                        new_obstacle = food.generate_new_position(obstacles + snake.body, snake.body)
                        obstacles.append(new_obstacle)

                    special_food = Food(board_size, obstacles, snake.body)
                    special_food_timer = time.time() + 10

            if special_food and snake.body[0] == special_food.position:
                score += 3
                special_food = None
                special_food_timer = None

            if special_food and time.time() > special_food_timer:
                special_food = None

            if snake.check_collision(obstacles, board_size):
                high_score = max(high_score, score)
                return score

            
            snake_head_scaled = pygame.transform.scale(snake_head_image, (cell_size, cell_size))
            snake_segment_scaled = pygame.transform.scale(snake_segment_image, (cell_size, cell_size))

            
            screen.blit(background_image, (0, 0))

            
            screen.blit(snake_head_scaled, (snake.body[0][0] * cell_size, snake.body[0][1] * cell_size))

            
            for x, y in snake.body[1:]:
                screen.blit(snake_segment_scaled, (x * cell_size, y * cell_size))

            
            food_scaled = pygame.transform.scale(food_image, (cell_size, cell_size))
            screen.blit(food_scaled, (food.position[0] * cell_size, food.position[1] * cell_size))

            if special_food:
                special_food_scaled = pygame.transform.scale(special_food_image, (cell_size, cell_size))
                screen.blit(
                    special_food_scaled,
                    (special_food.position[0] * cell_size, special_food.position[1] * cell_size),
                )

       
            obstacle_scaled = pygame.transform.scale(obstacle_image, (cell_size, cell_size))
            for x, y in obstacles:
                screen.blit(obstacle_scaled, (x * cell_size, y * cell_size))

            
            draw_text(screen, f"Score: {score}", font, text_color, (10, 10), shadow_color)
            draw_text(screen, f"High Score: {high_score}", font, text_color, (10, 50), shadow_color)

            pygame.display.flip()
            clock.tick(speed)


    def show_game_over_screen(score):
        game_over_image = pygame.image.load("game_over_image.png")
        game_over_image = pygame.transform.scale(
            game_over_image, (board_size[0] * cell_size, board_size[1] * cell_size)
        )
        screen.fill((0, 0, 0))
        screen.blit(game_over_image, (0, 0))
        draw_text(screen, f"Score: {score}", font, text_color, (10, 10), shadow_color)
        draw_text(screen, f"High Score: {high_score}", font, text_color, (10, 50), shadow_color)
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