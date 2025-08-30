import pygame
import random

pygame.init()

cell_size = 20

rows = 15
cols = 30

snake = [(10, 9), (10, 8), (10, 7)]
food = (random.randint(0, cols - 1), random.randint(0, rows - 1))
direction = (1, 0)
score = 0

screen = pygame.display.set_mode((cols * cell_size, rows * cell_size))
pygame.display.set_caption("Snake Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


def draw():
    screen.fill(BLACK)

    for x, y in snake:
        pygame.draw.rect(screen, GREEN, (x * cell_size, y * cell_size, cell_size, cell_size))

    fx, fy = food
    pygame.draw.rect(screen, RED, (fx * cell_size, fy * cell_size, cell_size, cell_size))

    pygame.display.update()


def move_snake():
    global snake, food, score
    head_x, head_y = snake[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)

    if new_head in snake:
        return False

    if not (0 <= new_head[0] < cols) or not (0 <= new_head[1] < rows):
        return False

    snake.insert(0, new_head)

    if new_head == food:
        score += 1
        while True:
            food = (random.randint(0, cols - 1), random.randint(0, rows - 1))
            if food not in snake:
                break
    else:
        snake.pop()

    return True


key_map = {
    pygame.K_w: (0, -1),
    pygame.K_UP: (0, -1),
    pygame.K_s: (0, 1),
    pygame.K_DOWN: (0, 1),
    pygame.K_d: (1, 0),
    pygame.K_RIGHT: (1, 0),
    pygame.K_a: (-1, 0),
    pygame.K_LEFT: (-1, 0)
}

opposite_dir = {
    (0, -1): (0, 1),
    (0, 1): (0, -1),
    (1, 0): (-1, 0),
    (-1, 0): (1, 0)
}


def handlel_keys():
    global direction
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key in key_map:
                new_dir = key_map[event.key]
                if new_dir != opposite_dir[direction]:
                    direction = new_dir
    return True


clock = pygame.time.Clock()
running = True

while running:
    clock.tick(10)
    running = handlel_keys()
    if not move_snake():
        print("Game Over")
        break
    draw()

pygame.quit()



