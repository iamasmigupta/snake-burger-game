import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Retro Snake Burger Edition")

BACKGROUND_COLOR = (174, 204, 97)  # #AECC61
HEAD_COLOR = (31, 42, 31)          # #1F2A1F
BORDER_COLOR = (0, 0, 0)
TEXT_COLOR = (31, 42, 31)

font = pygame.font.SysFont("Arial", 24, bold=True)
game_over_font = pygame.font.SysFont("Arial", 48, bold=True)

clock = pygame.time.Clock()
FPS = 12

snake = [(WIDTH//2, HEIGHT//2)]
direction = (0, 0)
score = 0
high_score = 0

food_pos = (random.randint(1, (WIDTH//GRID_SIZE)-2)*GRID_SIZE,
            random.randint(1, (HEIGHT//GRID_SIZE)-2)*GRID_SIZE)


def draw_border():
    pygame.draw.rect(screen, BORDER_COLOR, (0, 0, WIDTH, HEIGHT), 10)


def draw_snake():
    for segment in snake:
        pygame.draw.rect(screen, HEAD_COLOR, (segment[0], segment[1], GRID_SIZE, GRID_SIZE))


def draw_burger(x, y):

    # bottom bun
    pygame.draw.rect(screen, (210, 166, 121), (x, y+10, GRID_SIZE, 5))  # bun
    # patty
    pygame.draw.rect(screen, (77, 46, 31), (x, y+6, GRID_SIZE, 4))      # patty
    # lettuce
    pygame.draw.rect(screen, (76, 175, 80), (x-2, y+3, GRID_SIZE+4, 3)) # lettuce
    # top bun
    pygame.draw.rect(screen, (210, 166, 121), (x, y, GRID_SIZE, 5))     # top bun


def relocate_food():
    return (random.randint(1, (WIDTH//GRID_SIZE)-2)*GRID_SIZE,
            random.randint(1, (HEIGHT//GRID_SIZE)-2)*GRID_SIZE)


def draw_score():
    score_text = font.render(f"Score: {score}  High Score: {high_score}", True, TEXT_COLOR)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 10))


def show_game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (0, 0, 0))
    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2,
                                  HEIGHT//2 - game_over_text.get_height()//2))
    pygame.display.flip()
    pygame.time.delay(2000)


# Game loop
running = True
while running:
    screen.fill(BACKGROUND_COLOR)
    draw_border()
    draw_snake()
    draw_burger(*food_pos)
    draw_score()
    pygame.display.flip()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w) and direction != (0, GRID_SIZE):
                direction = (0, -GRID_SIZE)
            elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -GRID_SIZE):
                direction = (0, GRID_SIZE)
            elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != (GRID_SIZE, 0):
                direction = (-GRID_SIZE, 0)
            elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-GRID_SIZE, 0):
                direction = (GRID_SIZE, 0)

    # Update snake position
    if direction != (0, 0):
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        snake.insert(0, new_head)

        # Check collisions
        if (new_head[0] < 10 or new_head[0] > WIDTH-20 or
                new_head[1] < 10 or new_head[1] > HEIGHT-20 or
                new_head in snake[1:]):
            show_game_over()
            snake = [(WIDTH//2, HEIGHT//2)]
            direction = (0, 0)
            score = 0
            FPS = 12
            food_pos = relocate_food()

        # Food collision
        if abs(new_head[0] - food_pos[0]) < GRID_SIZE and abs(new_head[1] - food_pos[1]) < GRID_SIZE:
            score += 10
            if score > high_score:
                high_score = score
            food_pos = relocate_food()
            FPS += 0.2  # Increase speed slightly
        else:
            snake.pop()  # Remove last segment if no food eaten

    clock.tick(FPS)

pygame.quit()
sys.exit()
