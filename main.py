import pygame, random, time, runpy, os

pygame.init()

# Parametry labiryntu
WIDTH, HEIGHT = 40, 40
CELL_SIZE = 0
LINE_SIZE = 0
SIZE = 0

imag2 = False

def size_update():
    global CELL_SIZE, LINE_SIZE
    if SIZE == 0:
        CELL_SIZE = 10
        LINE_SIZE = 4
    if SIZE == 1:
        CELL_SIZE = 7
        LINE_SIZE = 3
    if SIZE == 2:
        CELL_SIZE = 5
        LINE_SIZE = 2
    if SIZE == 3:
        CELL_SIZE = 4
        LINE_SIZE = 1
    if SIZE == 4:
        CELL_SIZE = 3
        LINE_SIZE = 1
    if SIZE == 5:
        CELL_SIZE = 2
        LINE_SIZE = 1
    if SIZE == 6:
        CELL_SIZE = 1
        LINE_SIZE = 1

size_update()

win_width = WIDTH * CELL_SIZE
win_height = HEIGHT * CELL_SIZE

screen = pygame.display.set_mode((win_width, win_height), pygame.RESIZABLE)
pygame.display.set_caption(f'Labirynt {WIDTH}x{HEIGHT}')

import sys
sys.setrecursionlimit(1000)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

def init():
    global horizontal, vertical, visited
    horizontal = [[True for _ in range(WIDTH)] for _ in range(HEIGHT + 1)]
    vertical = [[True for _ in range(WIDTH + 1)] for _ in range(HEIGHT)]
    visited = [[False for _ in range(WIDTH)] for _ in range(HEIGHT)]
    
init()
clock = pygame.time.Clock()

def draw_maze():
    for y in range(HEIGHT + 1):
        for x in range(WIDTH):
            if horizontal[y][x]:
                pygame.draw.line(
                    screen, BLACK,
                    (x * CELL_SIZE, y * CELL_SIZE),
                    ((x + 1) * CELL_SIZE, y * CELL_SIZE), LINE_SIZE)
    for y in range(HEIGHT):
        for x in range(WIDTH + 1):
            if vertical[y][x]:
                pygame.draw.line(
                    screen, BLACK,
                    (x * CELL_SIZE, y * CELL_SIZE),
                    (x * CELL_SIZE, (y + 1) * CELL_SIZE), LINE_SIZE)
                
def generate_maze(x, y):
    stack = [(x, y)]
    visited[y][x] = True
    while stack:
        cx, cy = stack[-1]
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < WIDTH and 0 <= ny < HEIGHT and not visited[ny][nx]:
                # usuń odpowiednią ścianę jak dotąd...
                if dx == 1:  vertical[cy][cx+1] = False
                elif dx == -1: vertical[cy][cx] = False
                elif dy == 1: horizontal[cy+1][cx] = False
                elif dy == -1: horizontal[cy][cx] = False
                visited[ny][nx] = True
                stack.append((nx, ny))
                break  # Ważne! Pozostań na nowym polu, by zachować głębokościowy charakter DFS
        else:
            stack.pop()


def add_extra_branches(num_extra):
    for _ in range(num_extra):
        while True:
            x = random.randint(0, WIDTH - 2)
            y = random.randint(0, HEIGHT - 2)
            dirs = [(1,0), (0,1), (-1,0), (0,-1)]
            random.shuffle(dirs)
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                    # Sprawdź, czy jest ściana między (x, y) a (nx, ny)
                    wall_exists = False
                    if dx == 1 and vertical[y][x + 1]: wall_exists = True
                    elif dx == -1 and vertical[y][x]: wall_exists = True
                    elif dy == 1 and horizontal[y + 1][x]: wall_exists = True
                    elif dy == -1 and horizontal[y][x]: wall_exists = True
                    # Jeśli ściana istnieje, usuń ją
                    if wall_exists:
                        if dx == 1:
                            vertical[y][x + 1] = False
                        elif dx == -1:
                            vertical[y][x] = False
                        elif dy == 1:
                            horizontal[y + 1][x] = False
                        elif dy == -1:
                            horizontal[y][x] = False
                        break
            else:
                continue
            break


def load():
    init()
    generate_maze(WIDTH//2, HEIGHT//2)
    add_extra_branches((WIDTH*HEIGHT)//160)
def try_delete():
    try:
        os.system("if exist labirynt_rozwiazany.png del labirynt_rozwiazany.png")
    except:
        pass

load()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                try_delete()
                running = False
            elif event.key == pygame.K_F4:
                try_delete()
                load()
            elif event.key == pygame.K_F3:
                add_extra_branches(5)
            elif event.key == pygame.K_F9:
                pygame.image.save(screen, "screenshot.png")
                os.system("screenshot.png")
            elif event.key == pygame.K_F8:
                image = pygame.image.save(screen, "labirynt.png")
                runpy.run_path("rozwiaz.py")
                screen.fill(BLACK)
                pygame.display.update()
                time.sleep(0.250)
            elif event.key == pygame.K_F6:
                try_delete()
                if SIZE < 5:
                    SIZE += 1
                    size_update()
                    screen = pygame.display.set_mode((WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE))
                    pygame.display.set_caption(f'Labirynt {WIDTH}x{HEIGHT}')
                else:
                    SIZE = 0
                    size_update()
                    screen = pygame.display.set_mode((WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE))
                    pygame.display.set_caption(f'Labirynt {WIDTH}x{HEIGHT}')
            elif event.key == pygame.K_EQUALS:
                try_delete()
                screen.lock()
                if WIDTH < 1000 or HEIGHT < 1000:
                    WIDTH, HEIGHT = WIDTH+20, HEIGHT+20
                    screen = pygame.display.set_mode((WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE))
                    pygame.display.set_caption(f'Labirynt {WIDTH}x{HEIGHT}')
                    load()
            elif event.key == pygame.K_MINUS:
                try_delete()
                screen.lock()
                if WIDTH > 20 or HEIGHT > 20:
                    WIDTH, HEIGHT = WIDTH-20, HEIGHT-20
                    screen = pygame.display.set_mode((WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE))
                    pygame.display.set_caption(f'Labirynt {WIDTH}x{HEIGHT}')
                    load()
    if win_width != screen.get_width() or win_height != screen.get_height():
        try_delete()
        screen.lock()
        WIDTH = screen.get_width() // CELL_SIZE
        HEIGHT = screen.get_height() // CELL_SIZE

        win_width = WIDTH * CELL_SIZE
        win_height = HEIGHT * CELL_SIZE

        screen = pygame.display.set_mode((win_width, win_height), pygame.RESIZABLE)
        pygame.display.set_caption(f'Labirynt {WIDTH}x{HEIGHT}')
        load()
        
    screen.fill(WHITE)
    draw_maze()
    try:
        image = pygame.image.load("labirynt_rozwiazany.png")
        screen.blit(image, (0, 0))
        pygame.display.update()
    except:
        pass
    pygame.display.update()
    clock.tick(60)

pygame.quit()
