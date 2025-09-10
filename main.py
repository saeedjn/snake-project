import pygame
import random


pygame.init()
pygame.font.init()
clock = pygame.time.Clock()


cell_size = 10

rows = 50
cols = 60

settings = {
    "game_mode" : "wall",
    "speed_up_mode" : False,
    "random_wall_mode" : False,
    "random_wall_count" : 5,
    "player_name" : "Guest"
}

game_mode = settings["game_mode"]
random_wall_mode = settings["random_wall_mode"]
speed_up_mode = settings["speed_up_mode"]

snake = [(10, 9), (10, 8), (10, 7)]
food = (random.randint(0, cols - 1), random.randint(0, rows - 1))
direction = (1, 0)
random_wall_dest = []
number_of_random_wall = settings["random_wall_count"]
score = 0
base_speed = 10
running = True


screen = pygame.display.set_mode((cols * cell_size, rows * cell_size))
pygame.display.set_caption("Snake Game")

font = pygame.font.SysFont(None, 30)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (191, 187, 187)



def create_text(text,font_text,size,color,x,y):
    global screen
    font_text = pygame.font.SysFont(font_text, size)
    text = font_text.render(f"{text} ", True, color)
    rect = text.get_rect()
    rect.center = (x, y)
    screen.blit(text, rect)



def draw():
    screen.fill(BLACK)
    score_text = font.render(f"Score: {score}", True, WHITE)
    mode_wall_text = font.render(f"Mode: {game_mode}", True, WHITE)
    mode_speed_text = font.render(f"Speed: {base_speed}", True, WHITE)
    player_name_text = font.render(f"Name: {settings.get("player_name", "")}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(mode_wall_text, (120, 10))
    screen.blit(mode_speed_text, (280, 10))
    screen.blit(player_name_text, (10, 40))
    for x, y in snake:
        pygame.draw.rect(screen, GREEN, (x * cell_size, y * cell_size, cell_size, cell_size))

    fx, fy = food
    pygame.draw.rect(screen, RED, (fx * cell_size, fy * cell_size, cell_size, cell_size))

    if random_wall_mode:
        random_wall()
        create_random_walls()

    pygame.display.update()


def random_wall():
    len_wall = 4
    if random_wall_mode :
        while len(random_wall_dest) < number_of_random_wall :

            wall = []
            dir_wall = random.choice(["v", "h"])

            cell_start = (random.randint(0, cols - 7), random.randint(0, rows - 7))
            if cell_start in snake or cell_start == food:
                continue

            wall.append(cell_start)
            valid = True
            new_cell = False

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
                random_wall_dest.append(wall)

def move_snake():
    global snake, food, score, game_mode, base_speed, speed_up_mode, random_wall_dest
    head_x, head_y = snake[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)
    all_walls = [cell for wall in random_wall_dest for cell in wall]

    if new_head in snake:
        return False

    if new_head in all_walls:
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
        if speed_up_mode and base_speed < 25 and score % 5 == 0:
            base_speed += 1
        while True:
            food = (random.randint(0, cols - 1), random.randint(0, rows - 1))
            if food not in snake and food not in all_walls:
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
    global snake, direction, food, score, running, random_wall_dest
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
                    random_wall_dest = []
                    draw()
                    return "restart"
                if btn_e.collidepoint(event.pos):
                    running = False
                    return "exit"


def create_random_walls():
    all_walls = [cell for wall in random_wall_dest for cell in wall]
    for cell in all_walls:
        x, y = cell
        pygame.draw.rect(screen, WHITE, pygame.Rect(x * cell_size, y * cell_size,  cell_size, cell_size))

    pygame.display.update()


def setting_modal():
    global running, settings
    w,h = screen.get_size()
    modal_w, modal_h = w // 2, h // 3
    modal_x, modal_y = (w - modal_w) // 2, (h - modal_h) // 2
    border = 5
    player_name =  settings.get("player_name",'')
    input_box = pygame.Rect(modal_x+100, modal_y + 30, 140, 25)
    input_active_player = False
    padding = 0
    while True:
        screen.fill(BLACK)

        pygame.draw.rect(screen, GREEN, pygame.Rect(modal_x, modal_y, modal_w + border, modal_h + border))
        modal = pygame.draw.rect(screen, WHITE, pygame.Rect(modal_x, modal_y, modal_w, modal_h))


        create_text("Settings","Arial",20,RED,modal_x + modal_w // 2, modal_y + 20)
        create_text("Player Name: ","Arial",15,RED,modal_x + modal_w // 4 - 20, modal_y + 40)
        create_text("Game Mode: ","Arial",15,RED,modal_x + modal_w // 4 - 20 , modal_y + 70)
        create_text("Random Walls: ","Arial",15,RED,modal_x + modal_w // 4 + 150 , modal_y + 70)
        create_text("Speed Up Mode: ","Arial",15,RED,modal_x + modal_w // 4 - 10 , modal_y + 100)

        pygame.draw.rect(screen, WHITE if not input_active_player else GRAY, input_box)
        create_text(player_name, "Arial", 15, BLACK, input_box.x + 25 + padding, input_box.y + 12)

        btn_s = create_btn(modal,"left",0,GREEN, "Start")
        btn_e = create_btn(modal, "right",0,RED, "Quit")

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    input_active_player = True
                else:
                    input_active_player = False
            if event.type == pygame.KEYDOWN and input_active_player:
                if event.key == pygame.K_BACKSPACE and len(player_name) > 0:
                    player_name = player_name[:-1]
                    padding -= 3
                elif len(player_name) < 15:
                    player_name += event.unicode
                    padding += 3

            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.MOUSEBUTTONUP:
                if btn_s.collidepoint(event.pos):
                    settings["player_name"] = player_name
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
            clock.tick(base_speed)
            running = handle_keys()
            if not move_snake():
                game_over()
                modal_result = create_modal("Do you want Exit The Game? ")
                if modal_result == "quit" or modal_result == "exit":
                    break
                elif modal_result == "restart":
                    continue

            screen.fill(BLACK)
            draw()
    elif result_set == "exit":
        pygame.quit()


snake_game()
