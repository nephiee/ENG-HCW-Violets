import pygame
import random
import time

pygame.init()
width = 900
height = 500
reveal_font = pygame.font.Font(None, 80)
small_font = pygame.font.Font(None, 30)
screen = pygame.display.set_mode((width,height))

cols = 4
rows = 3
correct=[]
reveal = []
matches_found = 0
first_guess = [False, -1]
second_guess = [False, -1]
game_state = True
QUOTES = ["a violet in the youth of primy nature, forward, not permanent",
          "weigh what loss your honor may sustain",
          "keep you in the rear of your affection",
          "virtue itself ’scapes not calumnious strokes",
          "you do not understand yourself so clearly",
          "pooh, you speak like a green girl"]

FONT = pygame.font.Font(None, 36)
TEXT_COLOR = (40, 40, 60) 

def generate_board():
    global correct, reveal,matches_found, first_guess, second_guess
    correct = []
    correct = [i%6 for i in range(12)]
    random.shuffle(correct)
    reveal = [0,0,0,0,0,0,0,0,0,0,0,0]
    first_guess = [False, -1]
    second_guess = [False, -1]  
    matches_found = 0
    
def draw_text(surface, text, color, rect, font, aa=True):
    """Draw text inside a rect with word wrapping."""
    words = text.split(' ')
    lines = []
    line = ""
    for word in words:
        test_line = line + word + " "
        if font.size(test_line)[0] < rect.width - 20:  # leave some padding
            line = test_line
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)  # add the last line

    # Draw each line
    y_offset = 50
    for line in lines:
        line_surface = font.render(line.strip(), aa, color)
        line_rect = line_surface.get_rect(center=(rect.centerx, rect.y + y_offset + line_surface.get_height() // 2))
        surface.blit(line_surface, line_rect)
        y_offset += line_surface.get_height() 
    
def draw_board():
    global rows, cols,small_font, correct, first_guess, second_guess, reveal,matches_found
    board_list = []
    for i in range(cols):
        for j in range(rows):
            rect = pygame.Rect(i * (width // cols), j * (height // rows), width // cols, height // rows)
            pygame.draw.rect(screen, (200, 180, 220), rect, 10)
            board_list.append(rect)
            val = correct[j+i*rows]
            if( reveal[j+i*rows] == 1 ):
                draw_text(screen, QUOTES[val], (255, 0, 0), rect, small_font)
            if first_guess[0] and first_guess[1] == j+i*rows:
                draw_text(screen, QUOTES[val], (0, 0, 0), rect, small_font)
            if second_guess[0] and second_guess[1] == j+i*rows:
                draw_text(screen, QUOTES[val], (0, 0, 0), rect, small_font)
    return board_list

generate_board()
def matching(events):
    global correct, first_guess, second_guess, game_state, reveal,matches_found
    if(game_state==False):
        generate_board()
        game_state=True
        
    board = draw_board()
    
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for index, rect in enumerate(board):
                if rect.collidepoint(mouse_pos):
                    if reveal[index] == 1:
                        break
                    if first_guess[0] and second_guess[0]:
                        first_guess = [False, -1]
                        second_guess = [False, -1]
                    if not first_guess[0]:
                        first_guess[0] = True
                        first_guess[1] = index
                    elif not second_guess[0] and first_guess[0] and (index != first_guess[1]):
                        second_guess[0] = True
                        second_guess[1] = index
                        print(first_guess,second_guess)
                    if( correct[first_guess[1]] == correct[second_guess[1]] and (first_guess[1]!=-1 and second_guess[1]!=-1) ):
                        print(first_guess[1],second_guess[1])
                        reveal[first_guess[1]] = 1
                        reveal[second_guess[1]] = 1
                        matches_found+=1
                        print(reveal)
                        print("match")
                        print("matches found:", matches_found)
            
    tint = pygame.Surface((width, height), pygame.SRCALPHA) 
    tint.fill((235, 220, 247, 100))
    screen.blit(tint, (0, 0))
    
    
    msg = f"Match the quote to its pair. Press ESC to skip Stage"
    msg_render = FONT.render(msg, True, TEXT_COLOR)
    screen.blit(msg_render, (10, 10))
    
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_state = "win"
                return "win"
    
    
    if(matches_found==6):
        game_state=False
        return 'win'
    return '2'