import pygame
import sys
import time
from utils import load_config
from snake import Snake
from food import Food


def draw_text_box(screen, text, font, color, position, background_color,
                  padding=10, shadow_color=None):
    """
    Draw a text box on the screen with the given text, font, color, position,
    """
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    box_rect = pygame.Rect(
        position[0] - padding,
        position[1] - padding,
        text_rect.width + 2 * padding,
        text_rect.height + 2 * padding
    )

    pygame.draw.rect(screen, background_color, box_rect, border_radius=15)

    if shadow_color:
        shadow_rect = box_rect.move(2, 2)
        pygame.draw.rect(screen, shadow_color, shadow_rect, border_radius=15)

    screen.blit(text_surface, (box_rect.x + padding, box_rect.y + padding))


def show_welcome_screen(screen, font, board_size, cell_size):
    """
    Display the welcome screen with the game title.
    """
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
    """
    Main function that runs the game.
    """
    if len(sys.argv) < 2:
        print("Usage: python game.py <config_file>")
        sys.exit(1)

    pygame.init()
    pygame.mixer.init()

    eat_sound = pygame.mixer.Sound("eat_sound.wav")
    game_over_sound = pygame.mixer.Sound("game_over.mp3")
    pygame.mixer.music.load("background_music.mp3")
    pygame.mixer.music.play(-1)

    cell_size = 20
    config = load_config(sys.argv[1])
    board_size = config["board_size"]
    initial_obstacles = [tuple(obs) for obs in config["obstacles"]]

    screen = pygame.display.set_mode((board_size[0] * cell_size,
                                     board_size[1] * cell_size))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    font = pygame.font.Font("OpenSans-VariableFont_wdth,wght.ttf", 36)
    shadow_color = (0, 0, 0)
    text_color = (255, 255, 255)

    high_score = 0

    show_welcome_screen(screen, font, board_size, cell_size)

    scale_factor = 1.7

    snake_segment_image = pygame.image.load("snake_segment.png")
    snake_segment_image = pygame.transform.scale(
        snake_segment_image, (int(cell_size * scale_factor),
                              int(cell_size * scale_factor))
    )
    snake_head_image = pygame.image.load("snake_head.png")
    snake_head_image = pygame.transform.scale(
        snake_head_image, (int(cell_size * scale_factor),
                           int(cell_size * scale_factor))
    )
    food_image = pygame.image.load("food.png")
    food_image = pygame.transform.scale(
        food_image, (int(cell_size * scale_factor),
                     int(cell_size * scale_factor))
    )
    special_food_image = pygame.image.load("special_food.png")
    special_food_image = pygame.transform.scale(
        special_food_image,
        (int(cell_size * scale_factor),
         int(cell_size * scale_factor))
    )
    obstacle_image = pygame.image.load("stone.png")
    obstacle_image = pygame.transform.scale(
        obstacle_image,
        (int(cell_size * scale_factor),
         int(cell_size * scale_factor))
    )
    background_image = pygame.image.load("background.png")
    background_image = pygame.transform.scale(
        background_image,
        (board_size[0] * cell_size, board_size[1] * cell_size)
    )
    game_over_image = pygame.image.load("game_over_image.png")
    game_over_image = pygame.transform.scale(
        game_over_image, (board_size[0] * cell_size, board_size[1] * cell_size)
    )

    def start_game():
        """
        Start the game, have the logic for the game loop. Return the score.
        """
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
                    if event.key in [pygame.K_UP, pygame.K_DOWN,
                                     pygame.K_LEFT, pygame.K_RIGHT]:
                        direction = event.key

            snake.move(direction)

            if snake.body[0] == food.position:
                score += 1
                food.position = food.generate_new_position(obstacles,
                                                           snake.body)
                snake.grow()
                eat_sound.play()

                if score % 5 == 0 and score >= 5:
                    speed = min(15, speed + 1)
                    for _ in range(3):
                        new_obstacle = food.generate_new_position(obstacles +
                                                                  snake.body,
                                                                  snake.body)
                        obstacles.append(new_obstacle)

                    special_food = Food(board_size, obstacles, snake.body)
                    special_food_timer = time.time() + 10

            if special_food and snake.body[0] == special_food.position:
                score += 3
                special_food = None
                special_food_timer = None
                eat_sound.play()

            if special_food and time.time() > special_food_timer:
                special_food = None

            if snake.check_collision(obstacles, board_size):
                high_score = max(high_score, score)
                return score

            screen.blit(background_image, (0, 0))

            screen.blit(snake_head_image, (snake.body[0][0] * cell_size,
                                           snake.body[0][1] * cell_size))
            for x, y in snake.body[1:]:
                screen.blit(snake_segment_image, (x * cell_size,
                                                  y * cell_size))

            screen.blit(food_image, (food.position[0] * cell_size,
                                     food.position[1] * cell_size))

            if special_food:
                screen.blit(
                    special_food_image,
                    (special_food.position[0] * cell_size,
                     special_food.position[1] * cell_size),
                )

            for x, y in obstacles:
                screen.blit(obstacle_image, (x * cell_size, y * cell_size))
            '''
            # Afișează scorul și scorul maxim sus, unul lângă altul
            draw_text_box(
                screen,
                f"Score: {score}",
                font,
                text_color,
                (10, 10),
                background_color=(50, 50, 50),
                shadow_color=shadow_color
            )
            draw_text_box(
                screen,
                f"High Score: {high_score}",
                font,
                text_color,
                (200, 10),
                background_color=(50, 50, 50),
                shadow_color=shadow_color
            )
            '''
            pygame.display.flip()
            clock.tick(speed)

    def show_game_over_screen(score):
        """
        Show the game over screen with the score and high score.
        """
        pygame.mixer.music.stop()
        game_over_sound.play()
        screen.blit(game_over_image, (0, 0))

        draw_text_box(
            screen,
            f"Score: {score}",
            font,
            text_color,
            (10, 10),
            background_color=(50, 50, 50),
            shadow_color=shadow_color
        )
        draw_text_box(
            screen,
            f"High Score: {high_score}",
            font,
            text_color,
            (200, 10),
            background_color=(50, 50, 50),
            shadow_color=shadow_color
        )

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
                        pygame.mixer.music.play(-1)
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    while True:
        score = start_game()
        show_game_over_screen(score)


if __name__ == "__main__":
    main()
