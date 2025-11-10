
import pygame, random, sys

pygame.init()

# --- CONFIG ---
WIDTH, HEIGHT = 900, 500
CELL = 25               
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))

# colors (feel free to tweak)
BG = (40, 40, 60) 
WALL_COLOR = (40, 40, 60)    # walls
FLOOR_COLOR = (230, 230, 240)   # path background
PLAYER_COLOR = (200, 180, 220)   # player
EXIT_COLOR = (50, 200, 120)     # exit
TEXT_COLOR = (240, 240, 240)

FONT = pygame.font.Font(None, 36)

# --- Maze dimensions (in cells) ---
cols = WIDTH // CELL
rows = HEIGHT // CELL

# ensure odd dims for perfect-maze algorithm (carving on odd indices)
if cols % 2 == 0:
    cols -= 1
if rows % 2 == 0:
    rows -= 1

# center the maze if trimmed
offset_x = (WIDTH - cols * CELL) // 2
offset_y = (HEIGHT - rows * CELL) // 2

# --- Maze generation (grid of True=wall, False=floor) ---
def generate_maze(cols, rows):
    # initialize all walls
    grid = [[True for _ in range(cols)] for _ in range(rows)]

    def carve(cx, cy):
        dirs = [(2,0),(-2,0),(0,2),(0,-2)]
        random.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = cx + dx, cy + dy
            if 0 < nx < cols and 0 < ny < rows and grid[ny][nx]:
                # remove wall between
                grid[cy + dy//2][cx + dx//2] = False
                grid[ny][nx] = False
                carve(nx, ny)

    # start carving from (1,1)
    start_x, start_y = 1, 1
    grid[start_y][start_x] = False
    carve(start_x, start_y)
    return grid

# --- Build wall rect list from grid for collision testing ---
def wall_rects_from_grid(grid):
    rects = []
    for y in range(rows):
        for x in range(cols):
            if grid[y][x]:
                rect = pygame.Rect(offset_x + x*CELL, offset_y + y*CELL, CELL, CELL)
                rects.append(rect)
    return rects

# --- Player setup ---
player_radius = CELL // 3
player_speed = 3

def reset_game():
    global grid, walls, start_pos, exit_pos, player_pos, player_rect, game_state
    grid = generate_maze(cols, rows)
    walls = wall_rects_from_grid(grid)

    # start at (1,1) cell center
    start_cell = (1, 1)
    start_pos = (offset_x + start_cell[0]*CELL + CELL//2, offset_y + start_cell[1]*CELL + CELL//2)

    # exit at (cols-2, rows-2)
    exit_cell = (cols-2, rows-2)
    exit_pos = (offset_x + exit_cell[0]*CELL + CELL//2, offset_y + exit_cell[1]*CELL + CELL//2)

    player_pos = list(start_pos)
    player_rect = pygame.Rect(0,0, player_radius*2, player_radius*2)
    player_rect.center = player_pos
    game_state = "playing"  # "playing", "win", "lose"

reset_game()

def collided_with_wall(player_rect, walls):
    # precise test: check rect overlap with any wall rect
    for wr in walls:
        if player_rect.colliderect(wr):
            return True
    return False

flicker_timer = 0
flicker_interval = 0.05  # seconds between flickers
flicker_intensity = 20   # how strong the brightness change is
flicker_direction = 1    # to alternate between bright/dark
last_flicker_time = 0

def draw_maze():
    global flicker_timer, flicker_direction, last_flicker_time

    # Flicker effect (every few frames)
    now = pygame.time.get_ticks() / 1000.0  # seconds
    if now - last_flicker_time > flicker_interval:
        flicker_timer += flicker_direction * flicker_intensity
        # Clamp flicker value and reverse direction for pulsating effect
        if flicker_timer > 30 or flicker_timer < -30:
            flicker_direction *= -1
        last_flicker_time = now

    # Apply flicker to colors dynamically
    flicker_bg = (
        max(0, min(255, BG[0] + flicker_timer)),
        max(0, min(255, BG[1] + flicker_timer)),
        max(0, min(255, BG[2] + flicker_timer))
    )
    flicker_wall = (
        max(0, min(255, WALL_COLOR[0] + flicker_timer // 2)),
        max(0, min(255, WALL_COLOR[1] + flicker_timer // 2)),
        max(0, min(255, WALL_COLOR[2] + flicker_timer // 2))
    )

    # draw floor background
    screen.fill(flicker_bg)
    for y in range(rows):
        for x in range(cols):
            cell_rect = pygame.Rect(offset_x + x*CELL, offset_y + y*CELL, CELL, CELL)
            if grid[y][x]:
                pygame.draw.rect(screen, flicker_wall, cell_rect)
            else:
                pygame.draw.rect(screen, FLOOR_COLOR, cell_rect)

    # draw exit cell overlay
    exit_rect = pygame.Rect(exit_pos[0] - CELL//2, exit_pos[1] - CELL//2, CELL, CELL)
    pygame.draw.rect(screen, EXIT_COLOR, exit_rect)


    
def draw_player():
    pygame.draw.circle(screen, PLAYER_COLOR, (int(player_pos[0]), int(player_pos[1])), player_radius)

game_state = "playing"
running= True


def maze(events):
    global player_pos, player_rect, game_state, running

    if game_state == "playing":
        keys = pygame.key.get_pressed()
        vx = vy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            vx = -player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            vx = player_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            vy = -player_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            vy = player_speed

        # move in x, check collision, then y
        player_pos[0] += vx
        player_rect.centerx = int(player_pos[0])
        if collided_with_wall(player_rect, walls):
            game_state = "lose"

        player_pos[1] += vy
        player_rect.centery = int(player_pos[1])
        if collided_with_wall(player_rect, walls):
            game_state = "lose"

        # win check: reached exit area (use distance)
        dx = player_pos[0] - exit_pos[0]
        dy = player_pos[1] - exit_pos[1]
        if (dx*dx + dy*dy) <= (player_radius + CELL//4)**2:
            game_state = "win"

    draw_maze()
    draw_player()
    
    msg = f"Reach the exit without touching walls. Press ESC to skip Stage"
    msg_render = FONT.render(msg, True, TEXT_COLOR)
    screen.blit(msg_render, (10, 10))
    
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_state = "win"
                return "win"

    # overlays for win/lose
    if game_state == "win":
        return "win"
    elif game_state == "lose":
        reset_game()
        return "lose"
        
    return '3'
