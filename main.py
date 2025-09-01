import pygame
import random

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()


cell_size = 10

rows = 50
cols = 60

game_mode = "tunnel"
random_wall_mode = False

snake = [(10, 9), (10, 8), (10, 7)]
food = (random.randint(0, cols - 1), random.randint(0, rows - 1))
direction = (1, 0)
random_wall_dest = []
number_of_random_wall = 0
score = 0
running = True


screen = pygame.display.set_mode((cols * cell_size, rows * cell_size))
pygame.display.set_caption("Snake Game")

font = pygame.font.SysFont(None, 30)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


def draw():
    screen.fill(BLACK)
    score_text = font.render(f"Score: {score}", True, WHITE)
    mode_wall_text = font.render(f"Mode: {game_mode}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(mode_wall_text, (120, 10))
    for x, y in snake:
        pygame.draw.rect(screen, GREEN, (x * cell_size, y * cell_size, cell_size, cell_size))

    fx, fy = food
    pygame.draw.rect(screen, RED, (fx * cell_size, fy * cell_size, cell_size, cell_size))

    pygame.display.update()


def random_wall():
    len_wall = 4
    if random_wall_mode :
        while number_of_random_wall > len(random_wall_dest) :

            wall = []
            dir_wall = random.choice(["v", "h"])

            cell_start = (random.randint(0, cols - 7), random.randint(0, rows - 7))
            if cell_start in snake or cell_start == food:
                continue

            wall.append(cell_start)
            valid = True
            new_cell = None

            for i in range(1, len_wall) :
                x,y = wall[-1]
                if dir_wall == "v":
                    new_cell = (x ,y + 1)
                    if new_cell in snake or new_cell == food or new_cell[1] >= rows:
                        valid = False
                        break
                elif dir_wall == "h":
                    new_cell = (x + 1 ,y)
                    if new_cell in snake or new_cell == food or new_cell[0] >= cols:
                        valid = False
                        break
                wall.append(new_cell)

            if valid:
                random_wall_dest.extend(wall)





def move_snake():
    global snake, food, score, game_mode
    head_x, head_y = snake[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)

    if new_head in snake:
        return False

    if game_mode == "wall" :
        if not (0 <= new_head[0] < cols) or not (0 <= new_head[1] < rows):
            return False
    elif game_mode == "tunnel":
        x,y = new_head
        if x < 0 :
            x = cols - 1
        elif x >= cols:
            x = 0

        if y < 0 :
            y = rows - 1
        elif y >= rows:
            y = 0

        new_head = (x,y)



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


def handle_keys():
    global direction
    start_dir = direction
    handled = False

    for event in pygame.event.get():
        pygame.time.wait(1)
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key in key_map and not handled:
                new_dir = key_map[event.key]
                if new_dir != opposite_dir[start_dir]:
                    direction = new_dir
                    handled = True
    return True

def game_over():
    text = font.render("Game Over", True, RED)
    w,h = screen.get_size()
    rect = text.get_rect()
    rect.center = (w // 2, h // 2)
    screen.blit(text, rect)
    pygame.display.update()
    pygame.time.wait(800)


def create_btn(modal,pos,padding ,color,msg):
    x,y,w,h = modal
    btn_w, btn_h = w // 4, h // 6
    if pos == "right" :
        btn_rect = pygame.Rect((x + w - btn_w  - 20) + padding , (y + h) - 40, btn_w, btn_h)
    else:
        btn_rect = pygame.Rect(x + 20 + padding , (y + h) - 40, btn_w, btn_h)

    pygame.draw.rect(screen,color, btn_rect)
    font_btn = pygame.font.SysFont("Arial", 20)
    text = font_btn.render(msg, True, BLACK)
    rect = text.get_rect()
    rect.center = btn_rect.center
    screen.blit(text, rect)
    return btn_rect

def create_modal(msg):
    global snake, direction, food, score, running
    w,h = screen.get_size()
    modal_w, modal_h = w // 2, h // 3
    modal_x, modal_y = (w - modal_w) // 2, (h - modal_h) // 2
    border = 5
    while True:
        pygame.draw.rect(screen, RED, pygame.Rect(modal_x, modal_y, modal_w + border, modal_h + border))
        modal = pygame.draw.rect(screen, WHITE, pygame.Rect(modal_x, modal_y, modal_w, modal_h))

        text = font.render(msg, True, RED)
        rect = text.get_rect()
        rect.center = (modal_x + modal_w // 2, modal_y + 20)
        screen.blit(text, rect)

        btn_r = create_btn(modal,"left",0, GREEN, "ReStart")
        btn_e = create_btn(modal,"right",0, RED, "Quit")

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.MOUSEBUTTONUP:
                if btn_r.collidepoint(event.pos):
                    snake = [(10, 9), (10, 8), (10, 7)]
                    food = (random.randint(0, cols - 1), random.randint(0, rows - 1))
                    direction = (1, 0)
                    score = 0
                    running = True
                    draw()
                    return "restart"
                if btn_e.collidepoint(event.pos):
                    running = False
                    return "exit"



def setting_modal():
    global running
    w,h = screen.get_size()
    modal_w, modal_h = w // 2, h // 3
    modal_x, modal_y = (w - modal_w) // 2, (h - modal_h) // 2
    border = 5
    font_btn = pygame.font.SysFont("Arial", 20)
    while True:
        screen.fill(BLACK)

        pygame.draw.rect(screen, GREEN, pygame.Rect(modal_x, modal_y, modal_w + border, modal_h + border))
        modal = pygame.draw.rect(screen, WHITE, pygame.Rect(modal_x, modal_y, modal_w, modal_h))

        text = font_btn.render("Settings", True, RED)
        rect = text.get_rect()
        rect.center = (modal_x + modal_w // 2, modal_y + 20)
        screen.blit(text, rect)

        btn_s = create_btn(modal,"left",0,GREEN, "Start")
        btn_e = create_btn(modal, "right",0,RED, "Quit")

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.MOUSEBUTTONUP:
                if btn_s.collidepoint(event.pos):
                    return "start"
                if btn_e.collidepoint(event.pos):
                    running = False
                    return "exit"



def snake_game():
    global running
    result_set = setting_modal()
    if result_set == "start":
        screen.fill(BLACK)
        pygame.display.update()
        while running:
            clock.tick(10)
            running = handle_keys()
            if not move_snake():
                game_over()
                modal_result = create_modal("Do you want Exit The Game? ")
                if modal_result == "quit" or modal_result == "exit":
                    break
                elif modal_result == "restart":
                    continue
            draw()
    elif result_set == "exit":
        pygame.quit()


snake_game()
