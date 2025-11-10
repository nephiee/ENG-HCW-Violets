import pygame
import random

# --- CONFIG ---
width = 900
height = 500
rows, cols = 4, 4 
BG_COLOR = (30, 30, 40)
TILE_COLOR = (200, 180, 220)
EMPTY_COLOR = (40, 40, 60)
TEXT_COLOR = (20, 20, 20)
FONT = pygame.font.Font(None, 72)
SMALL_FONT = pygame.font.Font(None, 32)

screen = pygame.display.set_mode((width, height))

tile_w = width // cols
tile_h = height // rows

# Game state
board = []           # flat list length rows*cols; 0 will be the empty tile
empty_index = None
animating = False
game_won = False


def index_to_pos(idx):
    return idx % cols, idx // cols

def pos_to_index(col, row):
    return row * cols + col


def neighbors(idx):
    """Return list of neighbor indices that can move into idx (up/down/left/right)."""
    col, row = index_to_pos(idx)
    res = []
    if col > 0: res.append(pos_to_index(col - 1, row))
    if col < cols - 1: res.append(pos_to_index(col + 1, row))
    if row > 0: res.append(pos_to_index(col, row - 1))
    if row < rows - 1: res.append(pos_to_index(col, row + 1))
    return res


def is_solvable(tiles):
    """
    Check solvability for sliding puzzle:
    - Count inversions; for even width boards, blank row matters.
    """
    arr = [t for t in tiles if t != 0]
    inv = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                inv += 1

    if cols % 2 == 1:
        return inv % 2 == 0
    else:
        blank_row_from_bottom = rows - (tiles.index(0) // cols)
        # if blank on even row from bottom, inversions must be odd
        if blank_row_from_bottom % 2 == 0:
            return inv % 2 == 1
        else:
            return inv % 2 == 0


def create_solved():
    """Return solved board (1..N-1, 0)."""
    n = rows * cols
    return list(range(1, n)) + [0]


def shuffle_board(moves=200):
    """Shuffle by making random legal moves starting from solved board to guarantee solvability."""
    global board, empty_index
    board = create_solved()
    empty_index = board.index(0)

    for _ in range(moves):
        nbrs = neighbors(empty_index)
        choice = random.choice(nbrs)
        # swap empty and choice
        board[empty_index], board[choice] = board[choice], board[empty_index]
        empty_index = choice


def reset_game():
    global game_won, animating
    shuffle_board()
    game_won = False
    animating = False


# --- DRAWING ---
def draw_board():
    screen.fill(BG_COLOR)
    for idx, val in enumerate(board):
        col, row = index_to_pos(idx)
        rect = pygame.Rect(col * tile_w + 10 // 2,
                           row * tile_h + 10 // 2,
                           tile_w - 10,
                           tile_h - 10)

        if val == 0:
            pygame.draw.rect(screen, EMPTY_COLOR, rect, border_radius=8)
        else:
            pygame.draw.rect(screen, TILE_COLOR, rect, border_radius=8)
            text = FONT.render(str(val), True, TEXT_COLOR)
            #text_rect = text.get_rect(center=rect.center)
            img = pygame.image.load(f"../violets/assets/jigsaw/{str(val)}.jpg").convert()
            img = pygame.transform.scale(img, (tile_w - 10, tile_h - 10))
            screen.blit(img, rect)
            #screen.blit(text, text_rect)

    # top instructions
    inst = SMALL_FONT.render("Click or use arrows to move tiles", True, (220, 220, 220))
    screen.blit(inst, (10, 10))

    if game_won:
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((10, 10, 10, 180))
        screen.blit(overlay, (0, 0))
        win_text = FONT.render("You Win!", True, (255, 255, 255))
        screen.blit(win_text, win_text.get_rect(center=(width // 2, height // 2 - 20)))
        sub = SMALL_FONT.render("Press R to play again", True, (255, 255, 255))
        screen.blit(sub, sub.get_rect(center=(width // 2, height // 2 + 40)))


# --- MOVEMENT LOGIC ---
def move_tile_at_index(idx):
    """
    If tile at idx is adjacent to empty, swap and return True.
    """
    global empty_index
    if idx == empty_index:
        return False
    if idx in neighbors(empty_index):
        board[empty_index], board[idx] = board[idx], board[empty_index]
        empty_index = idx
        return True
    return False


def try_move_direction(dx, dy):
    """Try move in a direction using arrow keys (dx, dy from empty tile)."""
    col, row = index_to_pos(empty_index)
    target_col, target_row = col + dx, row + dy
    if 0 <= target_col < cols and 0 <= target_row < rows:
        target_idx = pos_to_index(target_col, target_row)
        return move_tile_at_index(target_idx)
    return False


def check_win():
    """Return True if board is in solved state."""
    n = rows * cols
    for i in range(n - 1):
        if board[i] != i + 1:
            return False
    return board[-1] == 0


# --- MAIN ---
reset_game()
def jigsaw(events):
    global game_won
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()
            if not game_won:
                if event.key == pygame.K_RIGHT:
                    try_move_direction(1, 0)
                if event.key == pygame.K_LEFT:
                    try_move_direction(-1, 0)
                if event.key == pygame.K_DOWN:
                    try_move_direction(0, 1)
                if event.key == pygame.K_UP:
                    try_move_direction(0, -1)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_won:
            mx, my = event.pos
            col = mx // tile_w
            row = my // tile_h
            if 0 <= col < cols and 0 <= row < rows:
                idx = pos_to_index(col, row)
                moved = move_tile_at_index(idx)
                # ignore moved boolean if needed

    draw_board()
    return 'win' if game_won else '5'
